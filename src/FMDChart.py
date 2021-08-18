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

import json

from src.FMDConfig import config 


class FMDChart():
    
    chart_type = None
    player = None
    attrs = None

    chart = None
    chart_title = None

    def __init__(self, chart_type, player, attrs, chart_title=None):
        '''
        chart_type: indicates the type of chart we want to get
        player: it could be only one (vertical, horizontal, polar) or an array (heatmap)
        attrs: it may be wheter an array with the attributes we want to plot or a string indicating
               the attributes family. In this case, an array will be formed by getting the attributes 
               from config. 
        '''
        print(f'attrs: {attrs}. chart_type: {chart_type}')

        available_chart_types = {
            'vertical_bars':self.get_vertical_bars,
            'horizontal_bars':self.get_horizontal_bars,
            'polar':self.get_polar_chart, 
            'heatmap':self.get_heatmap
        }
        
        if chart_type not in available_chart_types.keys():
            raise Exception(f'{chart_type} is not a valid chart type. Please, choose one from {available_chart_types}')

        # When a attributes familiy name is passed as argument instead of a list of attributes
        if isinstance(attrs, str):
            attrs = config.config_json[attrs]

        self.chart_type = chart_type
        self.player = player
        self.attrs = attrs 
        self.chart = available_chart_types[chart_type]()



    # SINGLE PLAYERS CHARTS
    def get_vertical_bars(self, filename='vertical_bars'):

        '''
        Get vertical bars chart from PLOTLY.
        player: Player object whose attributes we want to plot using a vertical bars chart
        attrs: list of attributes to plot
        '''
        # Get "figure" object from plotly api
        fig = go.Figure(
            data=[go.Bar(x=self.attrs, y=self.player.reg[self.attrs])]
        )
        # Set yaxis range to 1-20 to match attributes range
        fig['layout']['yaxis'].update(range=[0, 20], autorange=False)

        # for plotly charts 
        return self.get_chart_soup(fig, filename)    

    def get_horizontal_bars(self, filename='horizontal_bars'):
        '''
        Get horizontal bars chart from BOKEH.
        player: Player object whose attributes we want to plot using a horizontal bars chart
        attrs: list of attributes to plot
        '''
        y = self.attrs
        right = self.player.reg[self.attrs]
        
        p = figure(
            x_range=(0,20),
            y_range=y, 
            title=self.chart_title,
            toolbar_location=None, 
            tools="",
            plot_width=250, 
            plot_height=300,

        )
        p.hbar(y=y, right=right, height=0.95, line_color='white', color ="green")    
        html = file_html(p, CDN, filename)
        return html

    def get_polar_chart(self, filename='line_polar'):
        # Returns html elements to render chart 
        # attrs: attributes to consider in chart
        # Get chart and save it to file
        '''
        Get polar chart from PLOTLY.
        player: Player object whose attributes we want to plot using a horizontal bars chart
        attrs: list of attributes to plot
        '''
        fig = px.line_polar(r=self.player.reg[attrs], theta=self.attrs, line_close=True, range_r=[0,20], title=self.title)
        return self.get_chart_soup(fig, filename)

    # MULTIPLE PLAYERS CHARTS
    def get_heatmap(self, filename='heatmap'):
        # y: players objects 
        # attrs: attributes to plot names
        z = []  # matrix of vector with attributes values
        
        if not isinstance(self.player, list):
            raise Exception('For heatmaps, an array of player is needed, not only one player')

        # For every player we want to plot, we create an array with his attributes values (based on attrs list)
        # Then, it's appended to z matrix, the matrix that will be used to form the heatmap.
        for p in self.player:
            z_p = []
            for at in self.attrs:
                z_p.append(p.reg[at])
            z.append(z_p)

        fig = go.Figure(data=go.Heatmap(
            z=z,
            x=self.attrs,
            y=[p.reg.Name for p in self.player],
            colorscale='greens',
            hoverongaps = False,

            zmin=1,
            zmax=20,

            colorbar={'title':self.chart_title},         
        ))
        # soup is composed by a div tag containing two scripts tag (very long the second one)
        return self.get_chart_soup(fig, filename)

    # AUXILIAR METHODS
    def get_chart_soup(self, fig, filename):
        # for plotly charts
        fig.write_html("charts/{}.html".format(filename))
        return BeautifulSoup(open("charts/{}.html".format(filename)).read(), 'html.parser').find('div')