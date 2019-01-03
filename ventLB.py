# -*- coding: utf-8 -*-




import dash
import dash_core_components as dcc
import dash_html_components as html
from dash_html_components import Div,H1
from textwrap import dedent as d

import plotly.graph_objs as go

from dash.dependencies import Input, Output
import json

from test_dash.main import app,dflb,dfmuz
from test_dash.custom_html_components import menu
from test_dash.main import app


# TODO: abandonner plots vent LB + muz synchros + roses des vents trop dur et pas intéret fou
# mieux : un plot avec vent min lac blanc et muzelle
# un deuxième avec max LB et muzelle
# un troisième vent moyen LB et muzelle
# SYNCHROS
# et par ailleurs :
# plot vents + rose des vents avec rose synchros mais pas de synchros entre
# plots (elle pourra se rajouter avec des callbacks MAIS OUI!)
# TODO : voir comment synchro les axes avec un callback (permet dans tous les
# cas de tirer parti du stylage par la lib csv plutôt que par plotly)


def wind_figure(df):
    tracemin = go.Scatter(x=df.index,
                        y=df.min10mnwindspeed,
                        mode='lines+markers',
                        marker={'opacity':0},
                        name='Min 10 min')
    tracemax = go.Scatter(x=df.index,y=df.max10mnwindspeed,
                        mode='lines',name='Max 10 min')
    traceavg = go.Scatter(x=df.index,y=df.windspeed,
                        mode='lines',name='Moyen 10 min')
    return go.Figure(data=[tracemin,tracemax,traceavg])


windlims = [(0,5),(5,8),(8,11),(11,100)]
windlegends = ['<5 m/s','5-8 m/s','8-11 m/s','>11 m/s']
windcolors = ['rgb(242,240,247)','rgb(203,201,226)','rgb(158,154,200)','rgb(106,81,163)']
centers = list(range(0,360,45)) # longueur 8
lsups = [(center + 22.5)%360 for  center in centers]
linfs = [(center - 22.5)%360 for  center in centers]
names = ['North', 'N-E', 'East', 'S-E', 'South', 'S-W', 'West', 'N-W']

def get_count(df,index):
    if index == 0:
        return len(df[(df.winddir < lsups[index]) | (df.winddir >= linfs[index])])
    return len(df[(df.winddir < lsups[index]) & (df.winddir >= linfs[index])])



def windrose(df):
    traces = []
    for lim,legend,color in zip(windlims,windlegends,windcolors):
        mini,maxi = lim
        r = [get_count(df[(df.windspeed < maxi) & (df.windspeed >=mini)],i) for i in range(8)]
        traces.append(
            go.Barpolar(
                r= r,
                text=names,
                name=legend,
                marker=dict(
                    color=color
                )
            ))
    layoutwind = go.Layout(polar = {'angularaxis' :{'rotation': 90}})
    return go.Figure(data = traces,layout = layoutwind)





gr_lb = dcc.Graph(id='wind-lb',
                  figure=wind_figure(dflb),
                  style={"width": "98%","height":"98%"})

gr_muz = dcc.Graph(id='wind-muz',
                   figure=wind_figure(dfmuz),
                   style={"width": "98%",'height':'98%'})



roselb = dcc.Graph(id='windrose',
                   figure = windrose(dflb),
                   style={"width": "98%","height":"98%"})

rosemuz = dcc.Graph(id='windrosemuz',
                    figure = windrose(dfmuz),
                    style={"width": "98%","height":"98%"})


# TODO : mettre les éléments de style dans le css mais seulement après avoir
# trouvé les bons réglages


layout = [
    Div(
    children=[
        Div(children=[
            html.P("Vent Lac Blanc",
                    style={
                        "color": "#2a3f5f",
                        "fontSize": "20px",
                        "textAlign": "center",
                        "marginBottom": "0",
                    }),
            gr_lb
        ],
            className="eight columns chart_div",
            ),
        Div(children=[roselb],className="four columns chart_div",
            )
    ],
    className ="row",
),
    Div(
    children=[
        Div(children=[gr_muz],className="eight columns chart_div",
            ),
        Div(children=[rosemuz],className="four columns chart_div",
            )
    ],
    className ="row",
),
]


    # Div([
        # Div([gr_lb],className="height columns"),
        # Div([roselb],className="four columns")
    # ],
        # className = "row")
    # Div([
        # Div(gr_muz,className="height columns"),
        # Div(rosemuz,className="four columns")
    # ],
        # className = "row"
    # )



def filter_df(df,datmin,datmax,windmin,windmax):
    Cdate = (df.index >= datmin) & (df.index <= datmax)
    Cspeed = (df.windspeed >= windmin) & (df.windspeed <= windmax)
    return df[Cdate & Cspeed]


@app.callback(
    Output('windrose', 'figure'),
    [Input('wind-lb', 'selectedData')])
def display_selected_data_lb(selectedData):
    if selectedData:
        datmin = min(selectedData['range']['x'])
        datmax = max(selectedData['range']['x'])
        windmin = min(selectedData['range']['y'])
        windmax= max(selectedData['range']['y'])
        data = filter_df(dflb,datmin,datmax,windmin,windmax)
    else:
        data = dflb
    return windrose(data)

# @app.callback(
    # Output('windrosemuz', 'figure'),
    # [Input('all-winds', 'selectedData')])
# def display_selected_data_muz(selectedData):
    # datmin,datmax = selectedData['range']['x']
    # windmin,windmax=selectedData['range']['y']
    # data = filter_df(dfmuz,datmin,datmax,windmin,windmax)
    # rosewind = getWindFigure(data)
    # return rosewind


if __name__ == '__main__':
    app.run_server(debug = True)


