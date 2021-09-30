import base64
import io
from datetime import datetime

import pandas as pd

from home.src.pdfhandler import PDFHandler
from home.src.detector import Detector
from home.src.report import Report

import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_table
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.express as px
import dash_bootstrap_components as dbc

external_stylesheets = [dbc.themes.LUMEN]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
        },
        multiple=True
    ),
    html.Div([]),
    html.Div([
        html.Div(id="output-filenames"),
        dbc.Button("Submit", id='submit-val', color="primary", block=True, n_clicks=0),
        dbc.Spinner(
            children=[html.Div(id='output-data-upload')],
            size="lg",
            color="primary",
            type="border",
            fullscreen=True,
        )
    ]),
])


def extract_filenames(list_of_filenames):
    df = pd.DataFrame({"FILENAMES": [filename for filename in sorted(list_of_filenames) if "pdf" in filename]})

    return html.Div([
        html.Center(html.P("The following files are up to process. Please, click the Submit button to start hunting.")),
        dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True),
    ])


def parse_contents(list_of_contents, list_of_filenames):
    handler_list = []

    for contents, filename in zip(list_of_contents, list_of_filenames):
        content_type, content_string = contents.split(',')

        decoded = base64.b64decode(content_string)

        try:
            if 'pdf' in filename:
                handler = PDFHandler(filename, io.BytesIO(decoded))
                handler_list.append(handler)
        except Exception as e:
            print(e)
            return html.Div([
                "There was an error processing a file. DupHunter only supports PDF files."
            ])

    # detector produces the raw results
    d = Detector(
        handler_list,
        # language=mode([handler.language for handler in handler_list])
        language='portuguese'
    )
    d.setup_pairs()
    results = d.process()
    metrics = results[0]
    excerpts = results[1]

    # report produces the raw pdf file
    # r = Report(
    #     "templates",
    #     pd.DataFrame({"FILENAMES": [filename for filename in sorted(list_of_filenames) if "pdf" in filename]}).to_html(),
    #     None,
    #     metrics.to_html,
    #     excerpts.to_html,
    # )

    # create divs to return
    metrics_table = html.Div([
        dbc.Table.from_dataframe(metrics, striped=True, bordered=True, hover=True),
    ])

    excerpts_table = html.Div([
        dbc.Table.from_dataframe(excerpts, striped=True, bordered=True, hover=True),
    ])

    # dateformat = "%Y%m%d_%H%M%S"
    # download_button = html.Div([
    #     dbc.Button("Download Report", id='button_down', color="primary", block=True, n_clicks=0),
    #      dcc.Download(id="download-report",
    #          #dcc.send_bytes(r.pdf, filename=f"duphunter_{datetime.now().strftime(dateformat)}", type='pdf')
    #     )
    # ])

    return html.Div([
        html.Br(),
        html.Center(html.H1("Similarity Analysis")),
        metrics_table,
        html.Br(),
        html.Center(html.H1("Excerpts under Suspicion")),
        excerpts_table,
        html.Br(),
        # html.Center(html.H1("Download full report")),
        # download_button,
    ])


@app.callback(Output('output-data-upload', 'children'),
              Input('submit-val', 'n_clicks'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              prevent_initial_call=True)
def update_output(n_clicks, list_of_contents, list_of_names):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'submit-val' in changed_id:
        if list_of_contents is not None:
            children = [parse_contents(list_of_contents, list_of_names)]
            return children
    return html.Div()


@app.callback(Output('output-filenames', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'))
def update_output(list_of_contents, list_of_names):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if "upload-data" in changed_id:
        if list_of_contents is not None:
            children = extract_filenames(list_of_names)
            return children
    return html.Div()


if __name__ == '__main__':
    app.run_server(debug=True)
