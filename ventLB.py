# -*- coding: utf-8 -*-




import dash
import dash_core_components as dcc
import dash_html_components as html
from dash_html_components import Div,H1
from textwrap import dedent as d

import plotly.graph_objs as go

from dash.dependencies import Input, Output,State
import json

from test_dash.main import app,dflb,dfmuz
from test_dash.custom_html_components import menu
from test_dash.main import app
import numpy as np


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
                  style={"width": "98%","height":"98%"},config={"displayModeBar":False})

gr_muz = dcc.Graph(id='wind-muz',
                   figure=wind_figure(dfmuz),
                   style={"width": "98%",'height':'98%'})

roselb = dcc.Graph(id='windroselb',
                   figure = windrose(dflb),
                   style={"width": "98%","height":"98%"})

rosemuz = dcc.Graph(id='windrosemuz',
                    figure = windrose(dfmuz),
                    style={"width": "98%","height":"98%"})


# TODO : mettre les éléments de style dans le css mais seulement après avoir
# trouvé les bons réglages


layout = [
    html.Button("Fire an event",id="button-event"),
    Div(
        [html.H2("Lac Blanc: force du vent et rose des vents")],
        className = "row"
    ),
    Div(
        children=[
            Div(children=[
                # html.P("Vent Lac Blanc",
                       # style={
                           # "color": "#2a3f5f",
                           # "fontSize": "20px",
                           # "textAlign": "center",
                           # "marginBottom": "0",
                       # }),
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
        [html.H2("Muzelle : force du vent et rose des vents")],
        className = "row"
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



def filter_df(df,
              datmin=None,
              datmax=None,
              windmin=-np.Infinity,
              windmax=np.Infinity):
    Cdate = np.ones(len(df.index),dtype=bool)
    if datmin:
        Cdate = Cdate & (df.index >= datmin )
    if datmax:
        Cdate = Cdate & (df.index <= datmax )
    Cspeed = (df.windspeed >= windmin) & (df.windspeed <= windmax)
    return df[Cdate & Cspeed]


# remarque: avoir comme inputs à la fois zoom et selection c'est pas dans la
# philosophie de dash ce serait faire dépendre l'état de l'historique des
# actions - (ie : la rose des vents serait mise à jour selon l'action qui a été
# déclenchée en dernier zoom ou selection)
# donc il faut 2 roses par exemple, ou se résoudre à n'avoir un CB que sur le
# zoom

# attention ne jamais retourner None dans un callback!!!
# (la figure reste mais on perd toute référence vers elle!!!)

@app.callback(
    Output('windroselb', 'figure'),
    [Input('wind-lb','relayoutData')])
def display_selected_data_lb(relayoutData):
    if not relayoutData:
        return windrose(dflb)
    axis_match ={'yaxis.range[1]': 'windmax',
                 'xaxis.range[0]': 'datmin',
                 'xaxis.range[1]': 'datmax',
                 'yaxis.range[0]': 'windmin'}
    limits = {axis_name: relayoutData[axis_lim]
              for axis_lim,axis_name in axis_match.items()
              if axis_lim in relayoutData}
    return windrose(filter_df(dflb,**limits))



@app.callback(
    Output('windrosemuz', 'figure'),
    [Input('wind-muz','relayoutData'),Input('wind-lb','relayoutData')])
def display_selected_data_muz(relayoutData,relayoutLB):
    if not relayoutData:
        return windrose(dflb)
    axis_match ={'yaxis.range[1]': 'windmax',
                 'xaxis.range[0]': 'datmin',
                 'xaxis.range[1]': 'datmax',
                 'yaxis.range[0]': 'windmin'}
    limits = {axis_name: relayoutData[axis_lim]
              for axis_lim,axis_name in axis_match.items()
              if axis_lim in relayoutData}
    return windrose(filter_df(dflb,**limits))


@app.callback(
    Output('wind-muz', 'figure'),
    [Input('wind-lb','relayoutData')],
    [State('wind-muz','relayoutData')])
def resize_muzelle(relayoutData,figure):
    new_figure = wind_figure(dfmuz)
    if not relayoutData:
        return new_figure
    if 'xaxis.range[0]' in relayoutData:
        new_figure['layout']['xaxis']['range'] = [
            relayoutData['xaxis.range[0]'],
            relayoutData['xaxis.range[1]']
        ]
    if 'yaxis.range[0]' in relayoutData:
        new_figure['layout']['yaxis']['range'] = [
            relayoutData['yaxis.range[0]'],
            relayoutData['yaxis.range[1]']
        ]
    return new_figure








