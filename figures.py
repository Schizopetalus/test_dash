# -*- coding: utf-8 -*-

import plotly.graph_objs as go


def time_shape(timemin,timemax):
    shape = {
        'type': 'rect',
        'xref': 'x',
        'yref': 'paper',
        'x0':timemin,
        'y0': 0,
        'x1': timemax,
        'y1': 1,
        'fillcolor': 'rgba(128, 0, 128, 0.7)',
        'opacity': 0.2,
        'line': {
            'width': 0,
        }
    }
    return shape


def wind_figure(df,times=None):
    tracemin = go.Scatter(x=df.index,
                        y=df.min10mnwindspeed,
                        mode='lines+markers',
                        marker={'opacity':0},
                        name='Min 10 min')
    tracemax = go.Scatter(x=df.index,y=df.max10mnwindspeed,
                        mode='lines',name='Max 10 min')
    traceavg = go.Scatter(x=df.index,y=df.windspeed,
                        mode='lines',name='Moyen 10 min')
    if times is None:
        return go.Figure(data=[tracemin,tracemax,traceavg])

    layout = {'shapes': [time_shape(time[0],time[1]) for time in times]}
    return go.Figure(data=[tracemin,tracemax,traceavg],layout=layout)





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

