from home.src.analyzer import Analyzer
from home.src.diff import Diff
from itertools import combinations
import pandas as pd


class Detector:
    def __init__(self, handler_list, language="english"):
        self.language = language
        self.handler_list = handler_list
        setup = self.setup_pairs()
        self.analyzer_list = setup[0]
        self.differs_list = setup[1]

    def setup_pairs(self):
        analyzer_list = []
        differs_list = []
        for pair in list(combinations(self.handler_list, 2)):
            analyzer_list.append(Analyzer(pair[0], pair[1], self.language))
            differs_list.append(Diff(pair[0], pair[1], self.language))
        return analyzer_list, differs_list

    def process(self):
        df_metrics = pd.DataFrame()
        df_excerpts = pd.DataFrame()

        for analyzer in self.analyzer_list:
            df_metrics = df_metrics.append(analyzer.extract_metrics())
        for differ in self.differs_list:
            df_excerpts = df_excerpts.append(differ.extract_excerpts())

        return df_metrics, df_excerpts
