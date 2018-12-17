# -*- coding: utf-8 -*-

import plotly.graph_objs as go

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash_html_components import Div,H1
from test_dash.main import dflb,dfmuz

# external_stylesheets = ["https://unpkg.com/purecss@1.0.0/build/pure-min.css"]
# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


tracetension = go.Scatter(x=dflb.index,
                      y=dflb.tensionmin,
                      mode='lines+markers',
                      marker={'opacity':0},
                      name='Tension (V)')

graph_tension = dcc.Graph(figure={
                           'data': [tracetension],
                           'layout': {'title': 'Tension Station Lac Blanc'}
                       })

layout = Div([
    Div(graph_tension)]
)

if __name__ == '__main__':
    app.run_server(debug = True)

