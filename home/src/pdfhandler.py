from pdfminer import high_level


class PDFHandler:
    def __init__(self, filename, file):
        self.filename = filename
        self.text = high_level.extract_text(file)

    def __str__(self):
        return self.filepath
