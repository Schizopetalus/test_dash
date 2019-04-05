# -*- coding: utf-8 -*-



import dash
from dash_table import DataTable
import pandas as pd
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go
from dash.dependencies import Input, Output,State
from dash.exceptions import PreventUpdate

from data_clb.data import read_observations
from utils import TileDiv,generate_layout
import json

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

table_brut = DataTable(
    id='table_brut',
    columns=[{"name": i, "id": i} for i in dflb.columns],
    data=dflb.to_dict("rows"),
    editable=False,
    filtering=True,
    style_table=base_style_table,
    style_cell=base_style_cell,
    style_header=base_style_header,
    css=base_css
)


table_corrige = DataTable(
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


app.layout = html.Div(
    [dcc.Store(id='data_cor',data=dfcor.to_dict())] +\
    generate_layout(
        TileDiv(html.Button('Copier HTN Brut',id='copy_brut_to_corrected'),nrows=3),
        TileDiv(html.Div(),nrows=9),
        TileDiv(gr_htn),
        TileDiv([table_brut],nrows=8),
        TileDiv([table_corrige],nrows=4),
        TileDiv(html.Div(id='output'))
    )
)


def read_store(stored_data):
    """
    @ stored_data dict (dans l'appli obtenu à partir de json.to_dict)
    """
    data_as_df = pd.DataFrame.from_dict(stored_data)
    conv_dict = {'date': pd.to_datetime}
    for column in data_as_df.columns:
        data_as_df[column] = conv_dict.get(
            column,pd.to_numeric)(data_as_df[column])
    return data_as_df

# @app.callback(Output('output', 'children'),
              # [Input('data_cor', 'modified_timestamp')],
              # [State('data_cor', 'data')])
# def print_data(ts, data):
    # if ts is None:
        # raise PreventUpdate
    # data = data or {}
    # datapds = pd.DataFrame.from_dict(data)
    # print(datapds.dtypes)
    # datapds.set_index('date',inplace=True)
    # return json.dumps(datapds.to_dict())


@app.callback(Output('data_cor', 'data'),
              [Input('copy_brut_to_corrected', 'n_clicks')],
              [State('data_cor','data')])
def raw2corrected(n_clicks,data_cor):
    with open('tests/client_side_data/data_cor.json','w') as f:
        json.dump(data_cor,f)
    print('Done')
    return data_cor
    # data_cor_pds = pd.DataFrame.from_dict(data_cor)
    # print(data_cor_pds.head())
    # data_cor_pds.set_index('date',inplace=True)
    # data_cor_pds.htn = dflb.htnavg
    # return data_cor_pds.reset_index().to_dict()



if __name__ == '__main__':
    app.run_server(debug=True)
