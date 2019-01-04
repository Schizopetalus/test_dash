# -*- coding: utf-8 -*-

import dash
import dash_core_components as dcc
from dash_html_components import Div,H1,Span,P
from dash.dependencies import Input, Output
from data_analysis_clb.data import read_observations
import json
from test_dash.figures import wind_figure
from test_dash.utils import generate_layout,TileDiv


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

apptest = dash.Dash(__name__,external_stylesheets=external_stylesheets)
server = apptest.server
# apptest.config.suppress_callback_exceptions = True

df = read_observations(['LB','MUZ'],2018)
df = df[df.index > '2018-12-01']
dflb = df[df.site == 'LB']

config={
            'edits': {
                'shapePosition': True
            }
        }

graphdcc = dcc.Graph(id='tested_graph',
                   figure=wind_figure(dflb,times=[('2018-12-12','2018-12-13')]),
                   style={"width": "98%",'height':'98%'},
                     config = config)

div0 = TileDiv([Span("Page de test des tracés", className='app-title')],
        className = "header")
div1 = TileDiv([graphdcc], nrows= 8, className =  'chart_div')
div2 = TileDiv([H1("Relayout data"),P(id='relayout-data')],nrows=4,className = 'chart_div')
div3 = TileDiv([P('some text')], className='chart_div')


apptest.layout = Div(
    generate_layout(div0,div1,div2,div3)
)


@apptest.callback(
    Output('relayout-data', 'children'),
    [Input('tested_graph', 'relayoutData')])
def display_selected_data(relayoutData):
    return json.dumps(relayoutData, indent=2)

# @apptest.callback(
    # Output('tested_graph','figure'),
    # [Input('tested_graph','selectedData')])
# def create_new_box(selectedData


if __name__ == '__main__':
    apptest.run_server(debug=True)
