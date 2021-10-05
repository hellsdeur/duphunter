import base64
import io

from home.src.pdfhandler import PDFHandler
from home.src.detector import Detector
from home.src.report import Report

from django_plotly_dash import DjangoDash
import dash_html_components as html
import dash_core_components as dcc
import dash_table
from dash.dependencies import Input, Output, State

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('upload', external_stylesheets=external_stylesheets)

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
    print("Waiting for input"),
    html.Div(id='output-data-upload'),
])


def parse_contents(list_of_contents, list_of_filename):
    handler_list = []

    for contents, filename in zip(list_of_contents, list_of_filename):
        content_type, content_string = contents.split(',')

        decoded = base64.b64decode(content_string)

        try:
            if 'pdf' in filename:
                handler = PDFHandler(filename, io.BytesIO(decoded))
                handler_list.append(handler)
        except Exception as e:
            print(e)
            return html.Div([
                'There was an error processing this file.'
            ])

    d = Detector(
        handler_list,
        # language=mode([handler.language for handler in handler_list])
        language='portuguese'
    )
    d.setup_pairs()
    results = d.process()
    metrics = results[0]
    excerpts = results[1]

    metrics_table = html.Div([
        dash_table.DataTable(
            style_data={
                'whiteSpace': 'normal',
                'height': 'auto',
            },
            data=metrics.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in metrics.columns]
        )
    ])

    excerpts_table = html.Div([
        dash_table.DataTable(
            style_data={
                'whiteSpace': 'normal',
                'height': 'auto',
            },
            data=excerpts.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in excerpts.columns]
        )
    ])

    return html.Div([metrics_table, excerpts_table])


@app.callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'))
def update_output(list_of_contents, list_of_names):
    if list_of_contents is not None:
        children = [parse_contents(list_of_contents, list_of_names)]
        return children
