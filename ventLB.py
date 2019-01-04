# -*- coding: utf-8 -*-

import dash_core_components as dcc
import dash_html_components as html
from dash_html_components import Div,H1
from dash.dependencies import Input, Output,State
from test_dash.main import app,dflb,dfmuz
from test_dash.figures import wind_figure,windrose
from test_dash.utils import generate_layout,TileDiv
import numpy as np


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


el1 = TileDiv([html.H2("Lac Blanc: force du vent et rose des vents")])
el2 = TileDiv([gr_lb],nrows=8,className ='chart_div')
el3 = TileDiv([roselb],nrows= 4,className='chart_div')
el4 = TileDiv([html.H2("Muzelle : force du vent et rose des vents")])
el5 = TileDiv([gr_muz],nrows= 8,className =  'chart_div')
el6 = TileDiv([rosemuz],nrows=4,className = 'chart_div')

layout = generate_layout(el1,el2,el3,el4,el5,el6)



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








