# fmdataset.py
import pandas as pd

from charts import get_line_polar_chart, get_heatmap, get_horizontal_bars, get_vertical_bars
from Player import Player
import pipeline





###########################################################################################
###########################################################################################
####### Search players  ###################################################################
###########################################################################################
###########################################################################################
def search_player_by_name():
    pass

def search_players(form, sort_by=None):
    # Returns a list of dicts

    return_df = None
    try:
        del form['Submit']
    except:
        pass
    query   =   ''
    for at in form.keys():
        if form[at]:
            if at == 'Age':
                query += '{} <= {} and '.format(at, form[at])
            elif at == 'Club':
                query += '{} == "{}" and '.format(at, form[at])
            elif at == 'Name':
                return_df 	=	pipeline.df[pipeline.df['Name'].str.match(form['Name'])] 
                break
            elif at == 'EndOfContract':
                # query = 'EndOfContract == "31/06/{}"    '.format(form[at], form[at])
                return_df 	=	pipeline.df[pipeline.df['EndOfContract'].str.match(form['EndOfContract'])] 
            else:
                query += '{} >= {} and '.format(at, form[at])
    if not isinstance(return_df, pd.DataFrame):
        return_df = pipeline.df.query(query[:-4]) 

    if sort_by and sort_by != 'None':
        return_df = sort_dataframe(return_df, by=sort_by)

    return players_dataframe_to_list(return_df) 




def players_dataframe_to_list(players_df):
    # Returns a list of dicts
    players_list = []
    list_ = [players_df.columns.values.tolist()] + players_df.values.tolist()
    cols  = list_[0]
    for player_reg in list_[1:]:
        player_dict = {}
        for ii in range(len(cols)):
            player_dict[cols[ii]] = player_reg[ii]
        players_list.append(player_dict)

    return players_list


def sort_dataframe(df, by=['PrimaryRating', 'BackgroundRating'], ascending=False):
    if ',' in by:
        by = [at.strip() for at in by.split(',')]
    return df.sort_values(by=by, ascending=ascending)



def get_search_attrs(search_form):
    #   Returns attrs used in search
    search_attrs = []
    for at in search_form.keys():
        if search_form[at]:
            search_attrs.append(at.strip())

    return search_attrs