import base64
import io
from statistics import mode

import pandas as pd

from src.pdfhandler import PDFHandler
from src.detector import Detector

import dash
from dash import html
from dash import dcc
from dash import dash_table
from dash.dependencies import Input, Output, State

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

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
            'margin': '10px'
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
    print(results)

    return html.Div([
        html.Div([
            dash_table.DataTable(
                data=results.to_dict('records'),
                columns=[{'name': i, 'id': i} for i in results.columns]
            )
        ])
    ])

@app.callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'))
def update_output(list_of_contents, list_of_names):
    if list_of_contents is not None:
        children = [parse_contents(list_of_contents, list_of_names)]
        return children


if __name__ == '__main__':
    app.run_server(debug=True)
