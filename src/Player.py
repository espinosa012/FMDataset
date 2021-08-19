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
			'EndOfContract':self.reg.EndOfContract,
			'WeeklyWage':self.reg.WeeklyWage,
		}

	def fulfill_attrs_dict(self, attr_list):
		# generic method to be called from others
		dict_to_return = {}
		for at in attr_list:
			dict_to_return[at] = self.reg[at]
		return dict_to_return

	
	# GAME ATTRIBUTES
	def get_technical_attrs(self):
		# leer desde config
		return self.fulfill_attrs_dict(config.config_json['technical_attrs'])
		
	def get_mental_attrs(self):
		# leer desde config
		return self.fulfill_attrs_dict(config.config_json['mental_attrs'])

	def get_physical_attrs(self):
		# leer desde config
		return self.fulfill_attrs_dict(config.config_json['physical_attrs'])

	def get_goalkeeper_attrs(self):
		# leer desde config
		return self.fulfill_attrs_dict(config.config_json['goalkeeper_attrs'])

	def get_background_attrs(self):
		# leer desde config
		return self.fulfill_attrs_dict(config.config_json['background_attrs'])

	def get_primary_attrs(self):
		# leer desde config
		return self.fulfill_attrs_dict(config.config_json['primary_attrs'])
		
	def get_hidden_attrs(self):
		# leer desde config
		return self.fulfill_attrs_dict(config.config_json['hidden_attrs'])
	
	def get_person_attrs(self):
		# leer desde config
		return self.fulfill_attrs_dict(config.config_json['person_attrs'])

	



	# SET PIECES
	'''
	Set pieces are sets of attributes with certain relationship between them
	'''
	def get_default_set_pieces(self):
		set_pieces_dict = {}
		for sp in config.config_json['default_set_pieces'].keys():
			set_pieces_dict[sp] = self.fulfill_attrs_dict(config.config_json['default_set_pieces'][sp])
		return set_pieces_dict

	def get_goalkeeper_set_pieces(self):
		set_pieces_dict = {}
		for sp in config.config_json['goalkeeper_set_pieces'].keys():
			set_pieces_dict[sp] = self.fulfill_attrs_dict(config.config_json['goalkeeper_set_pieces'][sp])
		return set_pieces_dict

	def get_custom_set_pieces(self):
		set_pieces_dict = {}
		for sp in config.config_json['custom_set_pieces'].keys():
			set_pieces_dict[sp] = self.fulfill_attrs_dict(config.config_json['custom_set_pieces'][sp])
		return set_pieces_dict


	# RATINGS
	def get_custom_rating(self, rating):
		pass

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

	# ABILITIES
	def get_abilities(self):
		ability_dict = {}
		for ab in config.config_json['abilities_attrs'].keys():
			ability_dict[ab] = self.fulfill_attrs_dict(config.config_json['abilities_attrs'][ab])
		return ability_dict


	# ROLES
	def get_roles(self):
		# returns a list with all available roles (defined in config.json), but not any attribute.
		return list(config.config_json['roles_attrs'].keys())

	def get_role_attrs(self, role):
		# return attrs dict for certain role, passed as argument
		role_dict = {}
		try:
			for at in config.config_json['roles_attrs'][role]:
				role_dict[at] = self.reg[at]
			return role_dict
		except Exception as e:
			raise Exception(f'Error getting {role} attrs: {e}')

	# PRESELECTION
	def save_player_to_list(self):
		# to add player to player's preselection
		preselection_file = open(config.config_json['preselection_file_path'], 'a')
		preselection_file.write('{}\n'.format(self.reg.UID))
		preselection_file.close()


	def remove_player_from_list(self):
		# preselection_file = open(config.config_json['preselection_file_path'], 'r+')
		# lines = [l.strip() for l in preselection_file.readlines()] 
		preselection_file = open(config.config_json['preselection_file_path'], 'r+')
		print(preselection_file.read().replace(str(self.reg.UID), ''))

		for l in preselection_file.readlines():
			if l.strip():
				preselection_file.write(l)
		preselection_file.close()
				
		


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