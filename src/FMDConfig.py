import json
import pandas as pd 



class FMDConfig():

	config_json = None
	players_df = None
	home_df = None

	def __init__(self):
		self.config_json = json.load(open('config.json', 'r'))
		# general players dataframe
		self.players_df = pd.read_csv(self.config_json['csv_path'], sep=';')
		# general players dataframe
		self.clubs_df = None
		# dataframe with platyers tom display in home page
		self.home_df = self.players_df.query(self.config_json['home_dataframe_query'])

config = FMDConfig()