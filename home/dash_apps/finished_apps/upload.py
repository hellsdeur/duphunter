from .utils import Utils
from datetime import datetime
import pandas as pd

from django_plotly_dash import DjangoDash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

external_stylesheets = [dbc.themes.LUMEN]

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
    dcc.Store(id="memory-output"),
    html.Div([
        html.Div(id="output-filenames"),
        dbc.Button("Submit", id='submit-val', color="primary", block=True, n_clicks=0),
        dbc.Spinner(
            children=[
                html.Div(id='output-processing'),
                html.Br(),
            ],
            size="lg",
            color="primary",
            type="border",
            fullscreen=True,
        ),
        dbc.Button("Download Full Report", id='button_down', color="primary", block=True, n_clicks=0),
        dcc.Download(id="download-report")
    ]),
])


@app.callback(Output('output-filenames', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'))
def update_filenames(list_of_contents, list_of_names, **kwargs):
    # changed_id = [p['prop_id'] for p in kwargs['callback_context'].triggered][0]
    # if "upload-data" in changed_id:
    #     if list_of_contents is not None:
    #         return Utils.extract_filenames(list_of_names)
    if list_of_contents is not None:
        return Utils.extract_filenames(list_of_names)
    return None


@app.callback(Output('memory-output', 'data'),
              Input('submit-val', 'n_clicks'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              prevent_initial_call=True)
def update_output(n_clicks, list_of_contents, list_of_names, **kwargs):
    if n_clicks is None:
        raise PreventUpdate
    changed_id = [p['prop_id'] for p in kwargs['callback_context'].triggered][0]
    if 'submit-val' in changed_id:
        if list_of_contents is not None:
            return Utils.parse_contents(list_of_contents, list_of_names)
    return None


@app.callback(Output('output-processing', 'children'),
              Input('memory-output', 'data'),
              Input('submit-val', 'n_clicks'),
              Input('button_down', 'n_clicks'),
              State('upload-data', 'filename'))
def process(data, sub_clicks, dow_clicks, list_of_filenames):
    if sub_clicks is None:
        raise PreventUpdate
    if dow_clicks is None:
        raise PreventUpdate
    if data is None:
        raise PreventUpdate

    metrics = pd.read_json(data["METRICS"], orient='split')
    excerpts = pd.read_json(data["EXCERPTS"], orient='split')
    fig = Utils.plot(metrics)

    return html.Div([
        html.Br(),
        html.Center(html.H1("Similarity Analysis")),
        dcc.Graph(figure=fig),
        dbc.Table.from_dataframe(metrics, striped=True, bordered=True, hover=True),
        html.Br(),
        html.Center(html.H1("Excerpts under Suspicion")),
        dbc.Table.from_dataframe(excerpts, striped=True, bordered=True, hover=True),
        html.Br(),
    ])


@app.callback(Output('download-report', 'data'),
              Input('button_down', 'n_clicks'),
              Input('memory-output', 'data'),
              State('upload-data', 'filename'))
def download_report(n_clicks, data, list_of_filenames, **kwargs):
    if n_clicks is None:
        raise PreventUpdate
    if data is None:
        raise PreventUpdate
    dateformat = "%Y%m%d_%H%M%S"
    metrics = pd.read_json(data["METRICS"], orient='split')
    excerpts = pd.read_json(data["EXCERPTS"], orient='split')
    fig = Utils.plot(metrics)
    report = Utils.report('home/dash_apps/finished_apps/templates', list_of_filenames, fig, metrics, excerpts)
    changed_id = [p['prop_id'] for p in kwargs['callback_context'].triggered][0]
    if 'button_down' in changed_id:
        return dcc.send_bytes(
            src=report.pdf,
            filename=f"hunt_{datetime.now().strftime(dateformat)}",
            type='pdf')
