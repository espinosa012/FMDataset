import pandas as pd
from src.Player import Player
# from Player_ import Player 
# import charts
# import config
import numpy as np
import pandas as pd
# from pipeline import *
from bokeh.plotting import figure, output_file, show
# from charts import *


def clean_column_names(mdf):
    d = {}
    for col in list(mdf.columns):
        if 'Unnamed:' in col:
            mdf.drop(col, axis='columns', inplace=True)
        else:
            d[col] = col.strip()
    mdf.rename(columns=d, inplace=True)
        
def rtf_to_csv(rtf_path, output_file):
    new_file = open(output_file, 'w+')

    for line in open(rtf_path, 'r').readlines():
        if '|' in line and '-------' not in line:
            clean_line = line.strip().replace('| ','|').replace(' |','|') + '\n'
            new_file.write(clean_line)


def get_squad_df(mdf, df):
    # df: general app dataframe
    # mdf: imported from game
    for uid in mdf.UID:
        pass
        # print(df.loc[:, 'UID'])
        # print(mdf.query('UID == {}'.format(uid)).iloc[0].to_dict())


uids = [1700454, 22041890, 27025428]
# players = [Player(home_df.query("UID == {}".format(uid)).iloc[0]) for uid in uids]
players = [Player(uid) for uid in uids]
attrs = ['Determination', 'Tackling', 'Pace', 'Passing', 'Acceleration']

# c = FMDChart('heatmap', players, attrs, 'class')players[0]
print(players[0].get_role_attrs(r))
