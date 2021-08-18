import json
from .FMDConfig import config
from .FMDChart import FMDChart

class Player():

	reg = None
	uid = None

	def __init__(self, uid):
		# reg: column from dataframe 
		self.reg = self.get_df_register_from_uid(uid)		
		self.uid = self.reg.UID


	def get_df_register_from_uid(self, uid):
		return config.players_df.query("UID == {}".format(uid)).iloc[0]



	# PLAYER BASIC INFO
	def get_basic_info(self):
		return {
			'UID':self.reg.UID,
			'Name':self.reg.Name,
			'Age':self.reg.Age,
			'Club':self.reg.Club,
			'Value':self.reg.Value,
		}

	def get_contract_info(self):
		return {
			'EndOfContract':'',
			'WeeklyWage':'',
		}

	
	# GAME ATTRIBUTES
	def get_technical_attrs(self):
		# leer desde config
		technical_attrs = {}
		
	def get_mental_attrs(self):
		# leer desde config
		mental_attrs = {}

	def get_physical_attrs(self):
		# leer desde config
		physical_attrs = {}

	def get_goalkeeper_attrs(self):
		# leer desde config
		goalkeeper_attrs = {}

	def get_background_attrs(self):
		background_attrs = {}

	def get_primary_attrs(self):
		primary_attrs = {}
		
	def get_hidden_attrs(self):
		hidden_attrs = {}

	def get_person_attrs(self):
		person_attrs = {}

	
	
	# RATINGS
	def get_technical_rating(self):
		pass

	def get_mental_rating(self):
		pass

	def get_physical_rating(self):
		pass

	def get_goalkeeper_rating(self):
		pass

	def get_background_rating(self):
		pass

	def get_primary_rating(self):
		pass

	def get_custom_ratings(self):
		# returns an array (or dict) with self defined rating (in case there are any)
		pass
	


	# PRESELECTION

	def save_player_to_list(self):
		# to add player to player's preselection
		pass

	def remove_player_from_list(self):
		pass


	# MORE
	def get_similar_players(self):
		# TODO: implement an algorithm to get similar players (based on position, attributes range, key attributes)
		pass

	def add_player_note(self, note):
		# note: string with the text we want to save about player
		pass


	# CHARTS
	def get_player_page_charts(self):
		# returns a dict with the charts that will be displayed at player page
		
		# this method is suscpetible to change if player page is changed
		header_charts = {
			'technical':FMDChart('horizontal_bars', self, 'technical_attrs', chart_title='Technical attributes').chart,
			'mental':FMDChart('horizontal_bars', self, 'mental_attrs').chart,
			'physical':FMDChart('horizontal_bars', self, 'physical_attrs').chart,
		}
		# if 'GK' in player.positions:
		if 'GK' in self.reg.Positions:
			header_charts['technical'] = FMDChart('horizontal_bars', self, 'goalkeeper_attrs')

	    # Player page default overview charts
		overview_charts = { # temporal, untested
			'primary':{
	            'title':'Primary attributes',
	            'chart':FMDChart('vertical_bars', self, 'primary_attrs').chart,
	        },
	        'background':{
	            'title':'Background attributes',
	            'chart':FMDChart('vertical_bars', self, 'background_attrs').chart,
	        },
	        'person':{
	            'title':'Person attributes',
	            'chart':FMDChart('vertical_bars', self, 'person_attrs').chart,	            
	        },
		}

		return {
	        'header_charts':header_charts,
	        'overview_charts':overview_charts,
    	}