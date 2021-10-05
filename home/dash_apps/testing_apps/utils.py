import base64
import io
from datetime import datetime
import pandas as pd

import dash_html_components as html
import dash_core_components as dcc
from plotly.subplots import make_subplots
import plotly.io as pio
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

from home.src.pdfhandler import PDFHandler
from home.src.detector import Detector
from home.src.report import Report


class Utils:
    @staticmethod
    def extract_filenames(list_of_filenames):
        df = pd.DataFrame({"FILENAMES": [filename for filename in sorted(list_of_filenames) if "pdf" in filename]})

        return html.Div([
            html.Center(html.P("The following files are up to process. " +
                               "Please, click the Submit button to start hunting.")),
            dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True),
        ])

    @staticmethod
    def parse_contents(list_of_contents, list_of_filenames):
        pdf_handlers = []

        for contents, filename in zip(list_of_contents, list_of_filenames):
            content_type, content_string = contents.split(',')

            decoded = base64.b64decode(content_string)

            try:
                if 'pdf' in filename:
                    handler = PDFHandler(filename, io.BytesIO(decoded))
                    pdf_handlers.append(handler)
            except Exception as e:
                print(e)
                return html.Div([
                    "There was an error processing a file. DupHunter only supports PDF files."
                ])

        # detector produces the raw results
        d = Detector(
            pdf_handlers,
            # language=mode([handler.language for handler in handler_list])
            language='portuguese'
        )
        d.setup_pairs()
        results = d.process()
        metrics = results[0]
        excerpts = results[1]

        # # create divs to return
        # metrics_table = html.Div([
        #     dbc.Table.from_dataframe(metrics, striped=True, bordered=True, hover=True),
        # ])
        #

        #
        # excerpts_table = html.Div([
        #     dbc.Table.from_dataframe(excerpts, striped=True, bordered=True, hover=True),
        # ])
        #
        # # report produces the raw pdf file
        #
        #
        # # r.save_pdf()
        #
        # dateformat = "%Y%m%d_%H%M%S"
        # download_button = html.Div([
        #     dbc.Button("Download Report", id='button_down', color="primary", block=True, n_clicks=0),
        #     dcc.Download(id="download-report",
        #                  data=dcc.send_bytes(
        #                      src=r.pdf,
        #                      filename=f"duphunter_{datetime.now().strftime(dateformat)}",
        #                      type='pdf')
        #                  )
        # ])
        #
        # return html.Div([
        #     html.Br(),
        #     html.Center(html.H1("Similarity Analysis")),
        #     plot_figs,
        #     metrics_table,
        #     html.Br(),
        #     html.Center(html.H1("Excerpts under Suspicion")),
        #     excerpts_table,
        #     html.Br(),
        #     html.Center(html.H1("Download full report")),
        #     download_button,
        # ])
        data = {"METRICS": metrics.to_json(orient='split'),
                "EXCERPTS": excerpts.to_json(orient='split')}

        return data

    @staticmethod
    def plot(metrics):
        fig = make_subplots(
            rows=len(metrics.index)//2, cols=2,
            subplot_titles=["and".join(pair.split('-'))
                            for pair in list(metrics["PAIR_OF_FILES"])],
            # shared_yaxes=True
        )

        i = j = 1
        for n in range(len(metrics)):
            row = metrics.iloc[n]

            plot = go.Bar(
                x=["JACCARD", "CONTAINMENT", "LCS"],
                y=row[["JACCARD (%)", "CONTAINMENT (%)", "LCS (%)"]],
                name="and".join(row["PAIR_OF_FILES"].split('-')),
                showlegend=False,
            )

            fig.append_trace(trace=plot, row=i, col=j)

            if j == 1:
                j += 1
            else:
                j = 1
                i += 1

        fig.update_yaxes(range=[0, 100])
        return fig

    @staticmethod
    def report(list_of_filenames, fig, metrics, excerpts):
        return Report(
            "templates",
            pd.DataFrame({"FILENAMES": [filename for filename in list_of_filenames if "pdf" in filename]}).to_html(),
            # pio.to_html(fig=fig),
            fig,
            metrics.to_html(),
            excerpts.to_html(),
        )
