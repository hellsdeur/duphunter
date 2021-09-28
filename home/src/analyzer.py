import nltk
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
import pandas as pd

nltk.download('punkt')
nltk.download('stopwords')


class Analyzer:
    def __init__(self, pdfhandler1, pdfhandler2, language="english"):
        self.language = language

        self.pdfhandler1, self.pdfhandler2 = pdfhandler1, pdfhandler2
        self.txt1, self.txt2 = pdfhandler1.text, pdfhandler2.text

        self.tokens_txt1 = self.tokenize(self.txt1)
        self.tokens_txt1 = self.filtering(self.tokens_txt1)

        self.tokens_txt2 = self.tokenize(self.txt2)
        self.tokens_txt2 = self.filtering(self.tokens_txt2)

    def tokenize(self, text):
        return word_tokenize(text, language=self.language)

    def filtering(self, tokens):
        stop_words = set(stopwords.words(self.language))
        punctuations = ['"', '.', '(', ')', ',', '?', ';', ':', "''", '``']

        return [t for t in tokens if t.lower() not in stop_words and t.lower() not in punctuations]

    def trigrams_similarity(self):
        count_similarities = 0

        trigrams_txt1 = []
        for i in range(len(self.tokens_txt1)-2):
            t = [self.tokens_txt1[i], self.tokens_txt1[i + 1], self.tokens_txt1[i + 2]]
            trigrams_txt1.append(t)

        trigrams_txt2 = []
        for i in range(len(self.tokens_txt2) - 2):
            t = [self.tokens_txt2[i], self.tokens_txt2[i + 1], self.tokens_txt2[i + 2]]
            trigrams_txt2.append(t)
            if t in trigrams_txt1:
                count_similarities += 1

        jaccard = count_similarities / (len(trigrams_txt1) + len(trigrams_txt2))
        containment = count_similarities / len(trigrams_txt2)

        return jaccard, containment

    # longest common subsequence for two sentences
    def lcs(self, l1, l2):
        s1 = self.tokenize(l1)
        s2 = self.tokenize(l2)

        dp = [[None] * (len(s1) + 1) for i in range(len(s2) + 1)]

        for i in range(len(s2)+1):
            for j in range(len(s1)+1):
                if i == 0 or j == 0:
                    dp[i][j] = 0
                elif s2[i-1] == s1[j-1]:
                    dp[i][j] = dp[i-1][j-1]+1
                else:
                    dp[i][j] = max(dp[i-1][j], dp[i][j-1])

        return dp[len(s2)][len(s1)]

    def lcs_score(self):
        sent_txt1 = sent_tokenize(self.txt1, language=self.language)
        sent_txt2 = sent_tokenize(self.txt2, language=self.language)

        max_lcs = 0
        sum_lcs = 0

        for l1 in sent_txt1:
            for l2 in sent_txt2:
                lcs_pair = self.lcs(l1, l2)
                max_lcs = max(max_lcs, lcs_pair)
            sum_lcs += max_lcs
            max_lcs = 0

        return sum_lcs/len(self.tokens_txt2)

    def extract_metrics(self):
        jaccard, containment = self.trigrams_similarity()
        lcs = self.lcs_score()

        dic = {
            "PAIR_OF_FILES": self.pdfhandler1.filename + " - " + self.pdfhandler2.filename,
            "JACCARD": jaccard,
            "CONTAINMENT": containment,
            "LCS": lcs
        }
        return pd.DataFrame([dic])
