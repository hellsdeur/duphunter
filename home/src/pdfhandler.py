from pdfminer import high_level
from textblob import TextBlob


class PDFHandler:
    def __init__(self, filename, file):
        self.filename = filename
        self.text = high_level.extract_text(file)
        self.language = TextBlob(self.text).detect_language()

    def __str__(self):
        return self.filepath
