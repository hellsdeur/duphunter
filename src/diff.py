import sys
import difflib
from pprint import pprint

import nltk
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords

from pdfhandler import PDFHandler


class Diff:
    def __init__(self, pdfhandler1, pdfhandler2, language="english"):
        self.language = language

        self.pdfhandler1, self.pdfhandler2 = pdfhandler1, pdfhandler2
        self.txt1, self.txt2 = pdfhandler1.text, pdfhandler2.text

        self.sent_txt1 = ["".join(sent.split('\n')) for sent in sent_tokenize(self.txt1, language=self.language)]
        self.sent_txt2 = ["".join(sent.split('\n')) for sent in sent_tokenize(self.txt2, language=self.language)]

    def diffs(self):
        similarity = []

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
                    similarity.append([self.sent_txt1[i], self.sent_txt2[j]])
        return similarity


f1 = open("../resources/7.pdf", 'rb')
f2 = open("../resources/8.pdf", 'rb')
p1 = PDFHandler("7.pdf", f1)
p2 = PDFHandler("8.pdf", f2)

d = Diff(p1, p2)
print(d.diffs())
