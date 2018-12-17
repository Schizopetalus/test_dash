# -*- coding: utf-8 -*-




import dash
import dash_core_components as dcc
import dash_html_components as html
from dash_html_components import Div,H1
from textwrap import dedent as d

import plotly.graph_objs as go

from dash.dependencies import Input, Output
import json
from test_plotly.windrose import getWindFigure
from test_plotly.plots import wind_min_max_avg_plot,multiple_wind_plot

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

# tracemin = go.Scatter(x=dflb.index,
                      # y=dflb.min10mnwindspeed,
                      # mode='lines+markers',
                      # marker={'opacity':0},
                      # name='Min 10 min')
# tracemax = go.Scatter(x=dflb.index,y=dflb.max10mnwindspeed,
                      # mode='lines',name='Max 10 min')
# traceavg = go.Scatter(x=dflb.index,y=dflb.windspeed,
                      # mode='lines',name='Moyen 10 min')


graph_wind = dcc.Graph(id='all-winds',
                       figure= multiple_wind_plot(dflb,dfmuz))


windlb = dcc.Graph(id='windrose',
                   figure = getWindFigure(dflb))

windmuz = dcc.Graph(id='windrosemuz',
                    figure = getWindFigure(dfmuz))



layout = Div([
        Div(graph_wind,className="pure-u-3-5"),
        Div(windlb,className="pure-u-2-5")],
        className = "pure-g")


def filter_df(df,datmin,datmax,windmin,windmax):
    Cdate = (df.index >= datmin) & (df.index <= datmax)
    Cspeed = (df.windspeed >= windmin) & (df.windspeed <= windmax)
    return df[Cdate & Cspeed]


@app.callback(
    Output('windrose', 'figure'),
    [Input('all-winds', 'selectedData')])
def display_selected_data_lb(selectedData):
    if selectedData:
        datmin = min(selectedData['range']['x'])
        datmax = max(selectedData['range']['x'])
        windmin = min(selectedData['range']['y'])
        windmax= max(selectedData['range']['y'])
        data = filter_df(dflb,datmin,datmax,windmin,windmax)
    else:
        data = dflb
    rosewind = getWindFigure(data)
    return rosewind

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


