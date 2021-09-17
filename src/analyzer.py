import nltk
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords

nltk.download('punkt')
nltk.download('stopwords')

class Analyzer:
    def __init__(self, txt1, txt2):
        self.txt1, self.txt2 = txt1, txt2

        self.tokens_txt1 = self.tokenize(txt1)
        self.tokens_txt1 = self.filtering(self.tokens_txt1)

        self.tokens_txt2 = self.tokenize(txt2)
        self.tokens_txt2 = self.filtering(self.tokens_txt2)

    @staticmethod
    def tokenize(text):
        return word_tokenize(text)

    @staticmethod
    def filtering(tokens, language="english"):
        stop_words = set(stopwords.words(language))
        punctuations = ['"', '.', '(', ')', ',', '?', ';', ':', "''", '``']

        return [t for t in tokens if t.lower() not in stop_words and t.lower() not in punctuations]

    def __str__(self):
        return '\n'.join(self.tokens_txt2)