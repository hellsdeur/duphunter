from home.src.analyzer import Analyzer
from home.src.diff import Diff
from itertools import combinations
import pandas as pd


class Detector:
    def __init__(self, handler_list, language="english"):
        self.language = language
        self.handler_list = sorted(handler_list, key=lambda x: x.filename)
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

        return self.normalize(df_metrics), df_excerpts

    @staticmethod
    def normalize(df):
        df_norm = pd.DataFrame()
        df_norm["PAIR_OF_FILES"] = df["PAIR_OF_FILES"]
        minmax = {col: {"min": min(df[col]), "max": max(df[col])} for col in df.columns if col != "PAIR_OF_FILES"}
        for col in df.columns:
            if col != "PAIR_OF_FILES":
                df_norm[col + " (%)"] = (df[col] - minmax[col]["min"]) / (minmax[col]["max"] - minmax[col]["min"]) * 100
        return df_norm.round(3)
