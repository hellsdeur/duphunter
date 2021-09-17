from catalog import Catalog
from pdfhandler import PDFHandler
from analyzer import Analyzer
from itertools import combinations


class Detector:
    def __init__(self, directory):
        self.catalog = Catalog(directory)
        self.handler_list = [PDFHandler(filepath) for filepath in self.catalog]
        self.analyzer_list = self.process_pairs()

    def process_pairs(self):
        analyzer_list = []
        for pair in list(combinations(self.handler_list, 2)):
            self.analyzer_list.append(Analyzer(pair[0].text, pair[1].text))
        return analyzer_list


d = Detector("../resources")
d.process_pairs()