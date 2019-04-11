# -*- coding: utf-8 -*-



import dash
from dash_table import DataTable
import pandas as pd
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go
from dash.dependencies import Input, Output,State
from dash.exceptions import PreventUpdate

# from data_clb.data import read_observations
from utils import TileDiv,generate_layout
import json

# Données réelles
# df = read_observations(['LB'],2018,get_ftp=False)
# dflb = df[df.index > '2019-02-01'].iloc[:50]
# dflb = df[df.index > '2019-02-01']
# dflb = dflb.reset_index()

# Données prises dans le fichier csv qui dumpe le dataframe précédent
dflb = pd.read_csv('dataframe_lb.csv')
dflb.date = pd.to_datetime(dflb.date)
del dflb['Unnamed: 0']

subset_columns = ['date','htnavg','htnmin','htnmax','htnstd','htn2avg','htn2min','htn2max','htn2std']
htn_cor_columns = ['date','htn','htn2']
dflb = dflb[subset_columns]
dfcor = pd.DataFrame(columns=htn_cor_columns)
dfcor.date = dflb.date

################## Les plots #######################

schtn = go.Scatter(
    x=dflb.date,y=dflb.htnavg,
    name = "HTN brut moyen LB",line = dict(color='black',width=2))
schtnmax = go.Scatter(x=dflb.date,y=dflb.htnmax,line = dict(color='lightgrey',width=2),name='HTN max')
schtnmin = go.Scatter(x=dflb.date,y=dflb.htnmin,line = dict(color='lightgrey',width=2),name='HTN min')

fightn = go.Figure([schtn,schtnmin,schtnmax])

gr_htn = dcc.Graph(id='plotbrut',
                   figure = fightn)

gr_htn_corrige = dcc.Graph(id='plotcorrige')


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
        TileDiv(gr_htn_corrige),
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
    return data_as_df.set_index('date').sort_index().reset_index()



############## Affichage du contenu des données corrigées côté client ##########
# table et graphique
# événement : mise à jour du store contenant les données corrigées
@app.callback([
    Output('table_cor', 'data'),
    Output('plotcorrige','figure')],
    [Input('data_cor', 'data')])
def update_rows(data_cor):
    data_cor_pds = read_store(data_cor)
    schtncor = go.Scatter(
        x=data_cor_pds.date,y=data_cor_pds.htn,
        name = "HTN corrigé LB",line = dict(color='black',width=2))
    fightncor = go.Figure([schtncor])
    return data_cor_pds.to_dict("rows"),fightncor


############## Initialisation des données corrigées stockées côté client ######
# à partir de htnavg brut
# événement : click sur bouton
# FIXME : après tout, avoir plusieurs boutons pour effectuer des actions
# successives n'est peut-être pas judicieux
# on pourrait (si utile ...) avoir une datatable qui mémorise tous les filtres
# qu'on veut appliquer aux données par exemple?
# ou simplement mémoriser une liste des traitements appliqués?
# en attendant, une seul bouton qui charge les données corrigées et effectue le
# filtrage
@app.callback(Output('data_cor', 'data'),
              [Input('copy_brut_to_corrected', 'n_clicks')],
              [State('data_cor','data')])
def update_local_data(n_clicks,data_cor):
    if n_clicks is None:
        raise PreventUpdate
    data_cor_pds = read_store(data_cor)
    data_cor_pds.set_index('date',inplace=True)
    a = data_cor_pds.join(dflb.set_index('date'))
    o = a[(a.htnstd <2) & (a.htnavg>=0) & (a.htnavg < 600)]
    data_cor_pds.htn = o.htnavg
    return data_cor_pds.reset_index().to_dict()


if __name__ == '__main__':
    app.run_server(debug=True)
