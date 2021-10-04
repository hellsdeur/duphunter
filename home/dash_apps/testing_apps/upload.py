from utils import Utils
from datetime import datetime

import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
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


@app.callback(Output('output-data-upload', 'children'),
              Input('submit-val', 'n_clicks'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              prevent_initial_call=True)
def update_output(n_clicks, list_of_contents, list_of_names):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'submit-val' in changed_id:
        if list_of_contents is not None:
            children = [Utils.parse_contents(list_of_contents, list_of_names)]
            return children
    return html.Div()


@app.callback(Output('output-filenames', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'))
def update_output(list_of_contents, list_of_names):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if "upload-data" in changed_id:
        if list_of_contents is not None:
            children = Utils.extract_filenames(list_of_names)
            return children
    return html.Div()

# @app.callbackcallback(Output('download-report', 'children'),
#                       Input('submit-val', 'n_clicks'))
# def download(n_clicks):
#     dateformat = "%Y%m%d_%H%M%S"
#     changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
#     if 'submit-val' in changed_id:
#         return dcc.send_bytes(
#             src=pdf_file,
#             filename=f"duphunter_{datetime.now().strftime(dateformat)}",
#             type='pdf')
#         )


if __name__ == '__main__':
    app.run_server(debug=True)
