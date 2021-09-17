from pdfminer import high_level


class PDFHandler:
    def __init__(self, filepath):
        self.filepath = filepath

    def extract_text(self):
        return high_level.extract_text(self.filepath)
