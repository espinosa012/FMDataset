import flask
import json 

import pandas as pd
from flask import Flask, render_template, redirect, url_for, request

from Player import Player
from config import *
import pipeline

app = Flask(
    __name__, 
    static_url_path='',
    static_folder='static',
    template_folder='templates'
)

app.config["DEBUG"] = True

# ROUTES
@app.route("/")
@app.route("/home")
@app.route("/index")
def home():
    players = []
    for ii in range(len(pipeline.home_df)):
        players.append(pipeline.home_df.iloc[ii])
    return render_template("index.html", players=players)


@app.route("/player")
def player():
    uid = int(request.args.get('uid'))

    template = 'player.html'
    player = get_player_by_uid(uid) #player object
    charts = get_player_template_charts(player)
    return render_template(
        template, 
        player=player, 
        charts=charts,
    )


@app.route("/similar-players")
def similar_players():
    return "similar ({})".format('uid')


@app.route("/add-player-to-preselection")
def add_player_to_preselection():
    preselection_file = open('preselection.txt', 'a')
    preselection_file.write('{}\n'.format(request.args.get('uid')))
    preselection_file.close()
    return '{} added to list, <a href="javascript:history.back()"> back to player page</a>'.format(request.args.get('uid'))
     


@app.route("/remove-player-from-preselection")
def remove_player_from_preselection():
    pass



@app.route("/listed-players")
def listed_players():
    players = []
    uids = [uid.strip() for uid in reversed(open('preselection.txt', 'r').readlines())]
    for uid in uids:
        players.append(pipeline.df.query('UID == {}'.format(uid)).iloc[0])
    return render_template('search_result.html', players=players)




@app.route("/search")
def search_players_page():
    return render_template('search_players.html')


@app.route("/search_result", methods=['POST', 'GET'])
def search_result():
    sort_by = dict(request.form)
    #   sort_by is dict
    if 'sort_by' not in sort_by.keys():
        sort_by = None  

    search_form = request.args.get('search_form')
    if not search_form:
        search_form = dict(request.form)

    #   We have to convert string to dict
    if isinstance(search_form, str):
        #   convert search form from string to dict
        search_form = json.loads(search_form.replace("'",'"'))    

    #   Sort by is a dit, so we cast to str
    if sort_by:
        sort_by = sort_by['sort_by']

    #   We get sorted players list to display on template
    players_list = search_players(search_form, sort_by)

    #   We get attributes used in search to display it
    search_attrs = get_search_attrs(search_form)

    return render_template('search_result.html', players=players_list, search_form=search_form, search_attrs=search_attrs)











if __name__ == '__main__':
    app.jinja_env.globals.update(len=len)
    app.jinja_env.globals.update(list=list)

    app.run(host="0.0.0.0", port=8000, debug=True)