# -*- coding: utf-8 -*-


import dash_html_components as html
from dash_html_components import Div,A,Ul,Li


def menu_item(name,url):
    return Li(
        A(children=name, className="pure-menu-link",href=url),
        className = "pure-menu-item"
    )

def menu(listlinks):
    return Div(
        Ul([menu_item(name,url) for (name,url) in listlinks],
           className = "pure-menu-list"),
        className = "pure-menu pure-menu-horizontal pure-menu-scrollable"
    )

