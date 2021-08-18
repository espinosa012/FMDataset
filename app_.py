import json
from flask import Flask, render_template, redirect, url_for, request
from src.FMDConfig import config
from src.Player import Player



app = Flask(
    __name__, 
    static_url_path='',
    static_folder='static',
    template_folder='templates'
)

app.config["DEBUG"] = True







#################	ROUTES 	 #####################	

@app.route("/")
@app.route("/home")
@app.route("/index")
def home():
    players = []
    for ii in range(len(config.home_df)):
        players.append(config.home_df.iloc[ii])
    
    # "players" is a list of 'pandas.core.series.Series', not a list of Player objects
    # This way, page loads much faster.
    return render_template("index.html", players=players)



@app.route("/player")
def player():
    uid = int(request.args.get('uid'))

    # template = 'player.html'
    # player = get_player_by_uid(uid) #player object
    player = Player(uid)
    charts = player.get_player_page_charts()
    
    return render_template(
        'player.html', 
        player=player, 
        charts=charts,
    )
    return str(player.reg)



########	PRESELECTION 	########
@app.route("/listed-players")
def listed_players():
	# display list of players in preselection by readiong uids from txt file
	return 'listed-players'

@app.route("/add-player-to-preselection")
def add_player_to_preselection():
    preselection_file = open('preselection.txt', 'a')
    preselection_file.write('{}\n'.format(request.args.get('uid')))
    preselection_file.close()
    return '{} added to list, <a href="javascript:history.back()"> back to player page</a>'.format(request.args.get('uid'))
     
@app.route("/remove-player-from-preselection")
def remove_player_from_preselection():
	# remove uid from file
    pass


########	SEARCH PLAYERS 	########
@app.route("/search")
def search_players_page():
    return render_template('search_players.html')

@app.route("/similar-players")
def similar_players():
    return "similar ({})".format('uid')




##########################################################

if __name__ == '__main__':
    app.jinja_env.globals.update(len=len)
    app.jinja_env.globals.update(list=list)
    app.run(host="0.0.0.0", port=8000, debug=True)