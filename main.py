# -*- coding: utf-8 -*-

import dash
# lecture des données
from data_analysis_clb.data import read_observations

external_stylesheets = ["https://unpkg.com/purecss@1.0.0/build/pure-min.css"]

app = dash.Dash(__name__,external_stylesheets=external_stylesheets)
server = app.server
app.config.suppress_callback_exceptions = True
print('passing through main')

df = read_observations(['LB','MUZ'],2018)
dflb = df[df.site == 'LB']
dfmuz = df[df.site == 'MUZ']


