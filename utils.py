# -*- coding: utf-8 -*-

from dash_html_components import Div

int2words = {
    1: "one",
    2: "two",
    3: "three",
    4: "four",
    5: "five",
    6: "six",
    7: "seven",
    8: "eight",
    9: "nine",
    10: "ten",
    11: "eleven",
    12: "twelve"
}

class LayoutRowException(Exception):

    pass




def generate_layout(*args):
    """
    *args : objets de type TileDiv
    """
    layout = []
    newline = Div([],className='row')
    cursor = 0
    for tdiv in args:
        cursor+=tdiv.nrows
        if cursor > 12:
            raise LayoutRowException('Number of rows must sum to 12 for each line')
        classTile = "%s columns"%(int2words[tdiv.nrows],)
        if 'className' in tdiv.__dict__:
            tdiv.className += " %s"%(classTile,)
        else:
            tdiv.className = classTile
        newline.children.append(tdiv)
        cursor %= 12
        if cursor == 0:
            layout.append(newline)
            del newline
            newline = Div([],className = 'row')
    return layout



class TileDiv(Div):

    def __init__(self, *args, nrows=12, **kwargs):
        super().__init__(*args,**kwargs)
        self.nrows = nrows


