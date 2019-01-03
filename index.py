# -*- coding: utf-8 -*-


import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from test_dash.main import app
from test_dash.custom_html_components import menu
from test_dash import ventLB,tensionsLB


app.layout = html.Div([html.Div(
            html.Span("Maintenance Col du Lac Blanc", className='app-title'),
    className="row header"),
    #tabs (exemple suivi salesforce crm de la gallerie dash)
    html.Div([
        dcc.Tabs(
            id='tabs',
            style={"height":"20","verticalAlign":"middle"},
            children=[
                dcc.Tab(label="Vents",value="wind_tab"),
                dcc.Tab(label="Tension",value="tension_tab")
            ],
            value='all_tabs'
        )
    ],
        className = "row tabs_div"
    ),
    html.Div(id="tab_content", className="row", style={"margin": "2% 3%"}),
    html.Link(href="https://use.fontawesome.com/releases/v5.2.0/css/all.css",rel="stylesheet"),
    html.Link(href="https://fonts.googleapis.com/css?family=Dosis", rel="stylesheet"),
    html.Link(href="https://fonts.googleapis.com/css?family=Open+Sans", rel="stylesheet"),
    html.Link(href="https://fonts.googleapis.com/css?family=Ubuntu", rel="stylesheet"),
])




@app.callback(Output('tab_content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == "wind_tab":
         return ventLB.layout
    elif tab == "tension_tab":
         return tensionsLB.layout
    else:
        return ventLB.layout



if __name__ == '__main__':
    app.run_server(debug=True)

