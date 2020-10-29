from MyPlayer import MyPlayer
from pipeline import df, home_df

from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import file_html
from bokeh.io import output_file, show

from pychartjs import BaseChart, ChartType, Color                                     

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.figure import Figure

import plotly.express as px
import plotly.graph_objects as go

from bs4 import BeautifulSoup
from mpld3 import save_html

import pipeline

# SINGLE PLAYERS CHARTS


def get_vertical_bars(player, attrs, filename='vertical_bars', title=None):
    # plotly
    # fig = px.bar(x=attrs, y=player.reg[attrs], title=title)
    # return get_chart_soup(fig, filename)
    fig = go.Figure(
        data=[
            go.Bar(x=attrs, y=player.reg[attrs])
        ]
    )
    fig['layout']['yaxis'].update(range=[0, 20], autorange=False)

    return get_chart_soup(fig, filename)

def get_horizontal_bars(player, attrs, title=None):
    # bokeh
    y = attrs
    right = player.reg[attrs]
    
    p = figure(
        x_range=(0,20),
        y_range=y, 
        title=title,
        toolbar_location=None, 
        tools="",
        plot_width=250, 
        plot_height=300,

    )
    p.hbar(y=y, right=right, height=0.95, line_color='white', color ="green")    
    html = file_html(p, CDN, "my plot")
    return html


def get_polar_chart(player, attrs, filename='line_polar', title=None):
    #   Returns html elements to render chart 
    # attrs: attributes to consider in chart
    #   Get chart and save it to file
    fig = px.line_polar(r=player.reg[attrs], theta=attrs, line_close=True, range_r=[0,20], title=title)
    return get_chart_soup(fig, filename)


# MULTIPLE PLAYERS CHARTS
def get_heatmap(players, attrs, filename='heatmap', title=None):
    #   z: matrix of vector with attributes values
    #   x: attributes names
    #   y: players names
    
    z = []
    for p in players:
        z_p = []
        for at in attrs:
            z_p.append(p[at])
        z.append(z_p)
    fig = go.Figure(data=go.Heatmap(
        z=z,
        x=attrs,
        y=[p.Name for p in players],
        colorscale='greens',
        hoverongaps = False,

        zmin=1,
        zmax=20,

        colorbar={'title':title} , 
        
    ))
    #   soup is composed by a div tag containing two scripts tag (very long the second one)
    return get_chart_soup(fig, filename)





# AUXILIAR FUNCTIONS

def get_chart_soup(fig, filename):
    #   for plotly charts
    fig.write_html("charts/{}.html".format(filename))
    return BeautifulSoup(open("charts/{}.html".format(filename)).read(), 'html.parser').find('div')
