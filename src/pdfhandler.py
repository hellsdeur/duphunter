from pdfminer import high_level


class PDFHandler:
    def __init__(self, filepath):
        self.filepath = filepath
        self.text = high_level.extract_text(self.filepath)

    def __str__(self):
        return self.filepath
