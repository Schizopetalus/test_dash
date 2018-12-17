# -*- coding: utf-8 -*-


import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from test_dash.main import app
from test_dash.custom_html_components import menu
from test_dash import ventLB,tensionsLB


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


listlinks = [('Vents','/wind'),('Tensions','/voltage')]


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/wind':
         return html.Div([
             menu(listlinks),
             ventLB.layout])
    elif pathname == '/voltage':
         return html.Div([
             menu(listlinks),
             tensionsLB.layout])
    else:
        return '404'



# @app.callback(Output('url', 'pathname'),
              # [Input('url', 'pathname')])
# def redirect(pathname):
    # # print(dcc.Location)
    # # if pathname == '/':
        # # return '/wind'
    # # else:
    # return pathname


if __name__ == '__main__':
    app.run_server(debug=True)

