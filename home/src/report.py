import io

from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from datetime import datetime
from io import BytesIO


class Report:
    def __init__(self, templates_folder, file_table, metrics_graphs, metrics_table, excerpts_table):
        self.templates_folder = templates_folder
        env = Environment(loader=FileSystemLoader(self.templates_folder))
        self.template = env.get_template("report.html")
        self.vars = {
            "file_table": file_table,
            "metrics_graphs": metrics_graphs.decode("ascii"),
            "metrics_table": metrics_table,
            "excerpts_table": excerpts_table,
        }
        self.html = self.generate_html()
        self.pdf = self.generate_pdf()

    def generate_html(self):
        return self.template.render(self.vars)

    def generate_pdf(self):
        b = io.BytesIO()
        HTML(string=self.html).write_pdf(b, stylesheets=[self.templates_folder + "/style.css"])
        return b.getvalue()

    def save_pdf(self):
        dateformat = "%Y%m%d_%H%M%S"
        HTML(string=self.html).write_pdf(
            target=f"duphunter_{datetime.now().strftime(dateformat)}.pdf",
            stylesheets=[self.templates_folder + "/style.css"]
        )
