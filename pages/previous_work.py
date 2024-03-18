import dash
from dash import html
from functions.variable_store import *

dash.register_page(__name__, path='/')

layout = html.Div([
    html.Div(children=[
        html.A(children="Educational patterning in biological health seven years apart: Findings from the Tromsø Study (2024)", 
        href="https://www.sciencedirect.com/science/article/pii/S0306453023006480?via%3Dihub#sec0010", 
        target="_blank", className="underline m-2"),
        html.A(children="Early-life inequalities and biological ageing: a multisystem Biological Health Score approach in Understanding Society",
        href="https://doi.org/10.1136/jech-2018-212010",
        target="_blank", className="underline m-2"),
    ], className="grid auto-rows-auto"),

    # html.Span(children="Descriptive Statistics", className=badgeList[0]),
    # html.Span(children="Data Exploration", className=badgeList[1]),
    # html.Span(children="Drivers of Change", className=badgeList[2]),
    # html.Span(children="Interactive Comparisons", className=badgeList[3]),

], className='text-center m-4')