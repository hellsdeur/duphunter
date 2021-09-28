import difflib

import nltk
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords


class Diff:
    def __init__(self, pdfhandler1, pdfhandler2, language="english"):
        self.language = language

        self.pdfhandler1, self.pdfhandler2 = pdfhandler1, pdfhandler2
        self.txt1, self.txt2 = pdfhandler1.text, pdfhandler2.text

        self.sent_txt1 = ["".join(sent.split('\n')) for sent in sent_tokenize(self.txt1, language=self.language)]
        self.sent_txt2 = ["".join(sent.split('\n')) for sent in sent_tokenize(self.txt2, language=self.language)]

    def extract_excerpts(self):
        excerpts = {"PAIR_OF_FILES": [],
                    "ORIGINAL_EXCERPT": [],
                    "SUSPECT_EXCERPT": []
                    }

        for i in range(len(self.sent_txt1)):
            for j in range(len(self.sent_txt2)):
                diff = difflib.unified_diff(self.sent_txt1[i], self.sent_txt2[j])

                n = 0
                result = ''
                for difference in diff:
                    n += 1
                    if n < 7:
                        continue
                    result += difference[1]

                if len(result) == 0:
                    excerpts["PAIR_OF_FILES"].append(self.pdfhandler1.filename + " - " + self.pdfhandler2.filename),
                    excerpts["ORIGINAL_EXCERPT"].append(self.sent_txt1[i])
                    excerpts["SUSPECT_EXCERPT"].append(self.sent_txt2[j])

        return pd.DataFrame(excerpts)
