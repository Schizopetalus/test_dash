# -*- coding: utf-8 -*-

# Voir :   https://dash.plot.ly/live-updates

import datetime
import dash
import dash_html_components as html

app = dash.Dash(__name__)
# app.layout = html.H1('The time is: ' + str(datetime.datetime.now()))

def serve_layout():
    return html.H1('The time is: ' + str(datetime.datetime.now()))


app.layout = serve_layout


if __name__ == '__main__':
    app.run_server(debug=True)
