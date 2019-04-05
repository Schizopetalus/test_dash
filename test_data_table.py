# -*- coding: utf-8 -*-



import dash
import dash_table
from dash_table import DataTable
import pandas as pd
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go

from data_clb.data import read_observations
from utils import TileDiv,generate_layout

df = read_observations(['LB'],2018,get_ftp=False)
# dflb = df[df.index > '2019-02-01'].iloc[:50]
dflb = df[df.index > '2019-02-01']
dflb = dflb.reset_index()
subset_columns = ['date','htnavg','htnmin','htnmax','htnstd','htn2avg','htn2min','htn2max','htn2std']
htn_cor_columns = ['date','htn','htn2']


dflb = dflb[subset_columns]

dfcor = pd.DataFrame(columns=htn_cor_columns)
dfcor.date = dflb.date

################## Les plots #######################

schtn = go.Scatter(
    x=dflb.index,y=dflb.htnavg,
    name = "HTN brut moyen LB",line = dict(color='black',width=2))
schtnmax = go.Scatter(x=dflb.index,y=dflb.htnmax,line = dict(color='lightgrey',width=2),name='HTN max')
schtnmin = go.Scatter(x=dflb.index,y=dflb.htnmin,line = dict(color='lightgrey',width=2),name='HTN min')

fightn = go.Figure([schtn,schtnmin,schtnmax])

gr_htn = dcc.Graph(id='plotbrut',
                   figure = fightn)



app = dash.Dash(__name__)

default_style_cell = {
        'whiteSpace': 'no-wrap',
        'overflow': 'hidden',
        'textOverflow': 'ellipsis',
        'minWidth':'60px','width':'60px','maxWidth':'60px',
    }

style_cell_no_date = [
    {'if':{'column_id':column}}.update(default_style_cell)
    for column in set(dflb.columns) - {'date'}]


base_style_table =  {
    'overflowY': 'scroll',
    'overflowX': 'scroll',
    # 'width':'1000px',
    'height':'400px'
}

base_style_cell={
    'whiteSpace': 'no-wrap',
    'overflow': 'hidden',
    'textOverflow': 'ellipsis',
    'minWidth':'60px','width':'60px','maxWidth':'60px',
    'textAlign':'left',
}

base_style_header={
    'backgroundColor': 'orange',
    'fontWeight': 'bold'
}

base_css=[
    {
        'selector': '.dash-cell div.dash-cell-value',
        'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
    }
]

table_brut = TileDiv(
    [
        dash_table.DataTable(
    id='table_brut',
    columns=[{"name": i, "id": i} for i in dflb.columns],
    data=dflb.to_dict("rows"),
    editable=True,
    filtering=True,
    style_table=base_style_table,
    style_cell=base_style_cell,
    style_header=base_style_header,
    css=base_css
)],
    nrows=8)



table_corrige = TileDiv(
    [
        dash_table.DataTable(
            id='table_cor',
            columns=[{"name": i, "id": i} for i in dfcor.columns],
            data=dfcor.to_dict("rows"),
            editable=True,
            filtering=True,
            style_table=base_style_table,
            style_cell=base_style_cell,
            style_header=base_style_header,
            css=base_css
        )
    ],
    nrows=4
)


app.layout = html.Div(
    generate_layout(
        TileDiv(gr_htn),
        table_brut,
        table_corrige
    )
)

if __name__ == '__main__':
    app.run_server(debug=True)
