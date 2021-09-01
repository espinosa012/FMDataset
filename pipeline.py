import pandas as pd 
from numpy import int64
import json

# Get dataframe from csv file

config_json = json.load(open("config.json", "r"))

df = pd.read_csv(config_json['csv_path'], sep=';')
home_df = df.query('Club ==  "FC Midtjylland"')

# Pipeline para agregar las columnas correspondientes a abilities, roles, attrs_averages.
# All existing positions
positions = config_json['positions']

# Game attributes
technical_attrs = config_json['technical_attrs']
mental_attrs = config_json['mental_attrs']
physical_attrs = config_json['physical_attrs']
goalkeeper_attrs = config_json['goalkeeper_attrs']

# Hidden attributes
hidden_attrs = config_json['hidden_attrs']
person_attrs = config_json['person_attrs']

# Background/primary
background_attrs = config_json['background_attrs']
primary_attrs = config_json['primary_attrs']

#Custom ratings
custom_ratings = config_json['custom_ratings']

# https://www.passion4fm.com/football-manager-player-attributes/
set_pieces = config_json['set_pieces']

# Some metrics only for goalkeepers
goalkeeper_set_pieces = config_json['goalkeeper_set_pieces']
 
# ver para qué se usa

attrs_average_dict	=	{
	'TechnicalRating' 	:	technical_attrs,
	'MentalRating' 		:	mental_attrs,
	'PhysicalRating' 	:	physical_attrs,
	'GoalkeeperRating'	:	goalkeeper_attrs,
	
	'BackgroundRating' 	:	background_attrs,	
	'PrimaryRating'	 	:	primary_attrs,
}


roles_dict = config_json['roles_attrs']
abilities_dict = config_json['abilities_attrs']



######################################################################################################
######################################################################################################
############	  PIPELINE METHODS
######################################################################################################
######################################################################################################
def get_monthly_wage(row):
	# Estimates monthly wage from weekly wage (avilable in csv)
	return round((float(row['WeeklyWage'])/7)*30, 2) 


def get_clubUID(row):
	# since players csv does not contain club uid info, we add it by merging from clubs csv file
	clubs_df = pd.read_csv('csv/clubs.csv', sep=';', encoding='utf-8')
	try:
		return clubs_df.query('Name == "{}"'.format(row['Club'])).iloc[0]['ClubUID']
	except:
		# sometimes, club uid is not found.
		return '-'

def get_rating(row, attrs):
	# Receives attrs list and assign to column the average value of all of them.
	rating = 0
	for at in attrs:
		rating += row[at]
	return round(rating/len(attrs), 3)

def pipeline(input_csv, output_csv):
	stages = [
		{'rating_name':'PrimaryRating', 'attrs':config_json['primary_attrs']},
		{'rating_name':'BackgroundRating', 'attrs':config_json['background_attrs']},

		{'rating_name':'TechnicalRating', 'attrs':config_json['technical_attrs']},
		{'rating_name':'MentalRating', 'attrs':config_json['mental_attrs']},
		{'rating_name':'PhysicalRating', 'attrs':config_json['physical_attrs']},
		{'rating_name':'GoalkeeperRating', 'attrs':config_json['goalkeeper_attrs']},
	]
	df = pd.read_csv(input_csv, sep=';')

	for ab in abilities_dict.keys():
		df[ab] = df.apply(get_rating, args=(abilities_dict[ab], ), axis=1)		
	df.apply(get_monthly_wage, axis=1)
	df.apply(get_clubUID, axis=1)
	df.to_csv(output_csv, sep=';')
