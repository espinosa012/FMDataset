import 		pandas 	as		pd 
from 		numpy 	import 	int64
#	Get dataframe from csv file
csv_path 	=	'csv/players.csv'
df 			=	pd.read_csv(csv_path, sep=';')
home_df 	= 	df.query('Club ==  "FC Midtjylland"')


#	Pipeline para agregar las columnas correspondientes a abilities, roles, attrs_averages.

#	All existing positions
positions 	= 	['GK','SW','DC','DR','DL','DM','MC','MR','ML','AMC','AMR','AML','ST']
#	Game attributes
technical_attrs = ['Corners','Crossing','Dribbling','Finishing','FirstTouch','FreeKicks','Heading','LongShots','LongThrows','Passing','PenaltyTaking','Tackling','Technique']
mental_attrs 	= ['Aggression','Anticipation','Bravery','Composure','Concentration','Vision','Decisions','Determination','Flair','Influence','OffTheBall','Positioning','Teamwork','WorkRate']
physical_attrs 	= ['Acceleration','Agility','Balance','Jumping','NaturalFitness','Pace','Stamina','Strength']
goalkeeper_attrs= ['Kicking','OneOnOnes','Reflexes','RushingOut','TendencyToPunch','Throwing']

#	Hidden attributes
hidden_attrs 	= ['Dirtiness', 'Consistency', 'InjuryProneness', 'Versatility', 'ImportantMatches']
person_attrs 	= ['Temperament', 'Sportsmanship', 'Professionalism', 'Pressure', 'Loyalty', 'Controversy', 'Ambition', 'Adaptability']

#	Background/primary
background_attrs 	= ['WorkRate', 'Concentration', 'Teamwork', 'Determination']
primary_attrs 		= ['Decisions', 'Technique', 'Anticipation', 'Flair']

#	Custom ratings
custom_ratings 	=	{
	'ICRCholo'			:	['Teamwork', 'Bravery', 'Acceleration', 'NaturalFitness'],
	'passion4fm_rate1'	:	['Anticipation', 'Decisions', 'Positioning', 'WorkRate', 'Teamwork'],
	'youth_development'	:	['Determination', 'Ambition', 'Professionalism'],
	'striker':				['FirstTouch', 'Passing', 'Dribbling', 'Finishing', 'OffTheBall', 'Anticipation', 'Bravery', 'Acceleration', 'Balance', 'Strength', 'Pace', 'Decisions'],
	'header_striker': 		['Heading', 'Bravery', 'Jumping', 'Strength']
}


# https://www.passion4fm.com/football-manager-player-attributes/
set_pieces 	=	{
	'DirectFreeKicks':['FreeKicks', 'LongShots', 'Finishing'],
	'IndirectFreeKicks':['FreeKicks', 'Crossing', 'Passing', 'Vision'],
	'Penalty':['PenaltyTaking', 'Composure', 'Technique', 'Finishing', 'Concentration'],
	'Defending':['Tackling', 'Tackling', 'Marking', 'Positioning'],
	'Physical':['Strength', 'Stamina', 'Balance', 'Agility'],
	'Speed':['Acceleration', 'Pace'],
	'VisionSetPiece':['Vision', 'Flair', 'Passing'],
	'Attacking':['Finishing', 'OffTheBall','Composure'],	#for strikers
	'TechniqueSetPiece':['Technique', 'FirstTouch', 'Dribbling'],
	'Aerial':['Heading', 'JumpingReach'],
	'Mental':['Determination', 'Decisions', 'Anticipation', 'Teamwork', 'Bravery', 'Concentration']
}	

# Some metrics only for goalkeepers
goalkeeper_set_pieces = {
	'ShotStopping':['Reflexes', 'OneOnOnes'],
	'AerialGK':['Reflexes', 'JumpingReach'],
	'Distribution':['Throwing', 'Kicking'],
	'PhysicalGK':['Balance', 'Agility', 'Strength']
}


attrs_average_dict	=	{
	'TechnicalRating' 	:	technical_attrs,
	'MentalRating' 		:	mental_attrs,
	'PhysicalRating' 	:	physical_attrs,
	'GoalkeeperRating'	:	goalkeeper_attrs,
	
	'BackgroundRating' 	:	background_attrs,	
	'PrimaryRating'	 	:	primary_attrs,
}

roles_dict		=	{
	'Targetman'				:['FirstTouch','Heading','Aggression','Bravery','Determination','Teamwork','WorkRate','Jumping','Strength'],
	'Poacher'				:['Dribbling','Finishing','FirstTouch','Anticipation','Composure','OffTheBall','Acceleration','Agility','Balance','Pace'],
	'CompleteForward'		:['Dribbling','Finishing','FirstTouch','Heading','LongShots','Passing','Technique','Anticipation','Composure','Decisions','Determination','OffTheBall','Teamwork','Acceleration','Agility','Balance','Jumping','Pace','Strength'],
	'Trequartista'			:['Finishing','FirstTouch','Passing','Technique','Anticipation','Composure','Flair','OffTheBall','Agility'],
	'AdvancedForward'		:['Crossing','Dribbling','Finishing','Heading','Anticipation','Composure','Flair','OffTheBall','WorkRate','Pace'],
	'InsideForward'			:['Dribbling','Passing','Decisions','Flair','OffTheBall','Teamwork','Acceleration','Pace'],
	'DeepLyingForward'		:['Dribbling','FirstTouch','Passing','Technique','Decisions','OffTheBall','Teamwork','Balance','Strength'],
	'Winger'				:['Crossing','Dribbling','Technique','Decisions','Flair','OffTheBall','Acceleration','Agility','Balance','Pace'],
	'DefensiveMidfielder'	:['Marking','Tackling','Concentration','Decisions','Positioning','Teamwork','WorkRate','Acceleration','Stamina','Strength'],
	'Anchorman'				:['Heading','Marking','Tackling','Anticipation','Concentration','Decisions','Determination','Positioning','WorkRate','Strength'],
	'DeepLyingPlaymaker'	:['Passing','Tackling','Technique','Composure','Decisions','Positioning','Teamwork','Strength'],
	'CentreMidfielder'		:['FirstTouch','Passing','Decisions','Determination','Positioning','Teamwork','WorkRate'],
	'AdvancedPlaymaker'		:['FirstTouch','Passing','Technique','Decisions','Flair','Teamwork'],
	'BallWinningMidfielder'	:['Marking','Tackling','Aggression','Bravery','Determination','Positioning','Teamwork','WorkRate','Stamina','Strength'],
	'BoxToBox'				:['Dribbling','Finishing','FirstTouch','Heading','LongShots','Marking','Passing','Technique','Anticipation','Bravery','Decisions','Determination','OffTheBall','Positioning','WorkRate','Acceleration','Stamina','Strength'],
	'WideMidfielder'		:['Crossing','Passing','Tackling','Anticipation','Decisions','Determination','OffTheBall','Teamwork','WorkRate','Stamina'],
	'AttackingMidfielder'	:['FirstTouch','Passing','Technique','Decisions','Flair','OffTheBall','WorkRate'],
	'CentreBack'			:['Heading','Marking','Tackling','Composure','Concentration','Decisions','Determination','Positioning','Jumping','Strength'],
	'BallPlayingDefender'	:['Heading','Marking','Passing','Tackling','Technique','Composure','Concentration','Decisions','Determination','Positioning','Jumping','Strength'],
	'LimitedDefender'		:['Heading','Marking','Tackling','Determination','Positioning','Jumping','Strength'],
	'Fullback'				:['Marking','Tackling','Anticipation','Concentration','Positioning','Teamwork','WorkRate','Acceleration','Pace','Stamina'],
	'Wingback'				:['Marking','Tackling','Decisions','Positioning','Teamwork','WorkRate','Acceleration','Pace','Stamina'],
	'Sweeper'				:['Heading','Marking','Passing','Tackling','Anticipation','Composure','Concentration','Decisions','Positioning','Acceleration','Balance','Jumping'],
	'Libero'				:['Dribbling','Heading','Marking','Passing','Tackling','Anticipation','Composure','Concentration','Decisions','Positioning','Teamwork','Acceleration','Balance','Jumping']
}


abilities_dict 	=	{
	'Intelligence'			: ['Vision', 'Anticipation', 'Flair', 'Teamwork', 'Decisions'], 
	'Focus'					: ['Concentration', 'Composure'], 
	'Endeavour'				: ['Bravery', 'WorkRate', 'Aggression', 'Determination'], 
	'Creativity'			: ['Vision', 'Anticipation', 'Flair', 'Teamwork', 'Decisions'], 
	'Movement'				: ['OffTheBall', 'Positioning', 'Anticipation', 'Teamwork', 'Decisions'], 
	'Awareness'				: ['Anticipation', 'Anticipation', 'Teamwork', 'Vision'], 
	'DecisionMaking'		: ['Flair', 'Decisions', 'Teamwork'], 
	'PhysicalPresence'		: ['Strength', 'WorkRate', 'Bravery', 'Determination', 'Balance', 'Aggression'], 
	'AerialPresence'		: ['Strength', 'WorkRate', 'Jumping', 'Bravery', 'Balance', 'Determination', 'Aggression'], 
	'Mobility'				: ['Acceleration', 'Pace', 'WorkRate', 'Agility', 'Determination'], 
	'OffTheBallMovement'	: ['Strength', 'Anticipation', 'Composure', 'OffTheBall', 'Jumping', 'WorkRate', 'Bravery', 'Balance', 'Teamwork', 'Determination', 'Concentration', 'Aggression', 'Decisions'], 
	'Control'				: ['Strength', 'Anticipation', 'Composure', 'Technique', 'Jumping', 'WorkRate', 'Bravery', 'Aggression', 'FirstTouch', 'Teamwork', 'Determination', 'Concentration', 'Balance', 'Vision', 'Flair', 'Decisions'], 
	'PassingAbility'		: ['Anticipation', 'Composure', 'Technique', 'Teamwork', 'Determination', 'Concentration', 'Passing', 'Vision', 'Flair', 'Decisions'], 
	'CrossingAbility'		: ['Vision', 'Anticipation', 'Composure', 'Technique', 'Passing', 'Determination', 'Crossing', 'Concentration', 'Teamwork', 'Flair', 'Decisions'], 
	'DribblingAbility'		: ['Strength', 'Anticipation', 'Composure', 'Technique', 'Dribbling', 'Jumping', 'WorkRate', 'Bravery', 'Aggression', 'Balance', 'Determination', 'Concentration', 'Decisions', 'Flair', 'Vision'], 
	'ShootingAbility'		: ['Anticipation', 'Composure', 'Technique', 'Determination', 'Concentration', 'Finishing', 'Decisions', 'Flair', 'LongShots', 'Vision'], 
	'HeadingAbility'		: ['Strength', 'Anticipation', 'Composure', 'Technique', 'Jumping', 'WorkRate', 'Bravery', 'Aggression', 'Balance', 'Teamwork', 'Determination', 'Concentration', 'Vision', 'Flair', 'Heading', 'Decisions'], 
	'HoldUpPlay'			: ['Anticipation', 'Composure', 'Composure', 'Strength', 'Bravery', 'Balance', 'Teamwork', 'Determination', 'WorkRate', 'Concentration', 'Aggression', 'Decisions'], 
	'MarkingAbility'		: ['Strength', 'Anticipation', 'Jumping', 'Composure', 'Positioning', 'Marking', 'Bravery', 'Balance', 'Teamwork', 'Determination', 'WorkRate', 'Concentration', 'Aggression', 'Decisions'], 
	'DefensivePositioning'	: ['Strength', 'Anticipation', 'Jumping', 'Composure', 'Composure', 'Positioning', 'WorkRate', 'Bravery', 'Balance', 'Teamwork', 'Determination', 'Concentration', 'Aggression', 'Decisions'], 
	'ClosingDownAbility'	: ['Strength', 'Anticipation', 'Jumping', 'Composure', 'Composure', 'Positioning', 'WorkRate', 'Bravery', 'Balance', 'Teamwork', 'Determination', 'Concentration', 'Aggression', 'Decisions'], 
	'TacklingAbility'		: ['Anticipation', 'Composure', 'Tackling', 'Strength', 'Bravery', 'Decisions', 'Determination', 'WorkRate', 'Concentration', 'Balance', 'Aggression'], 
	'InterceptingAbility'	: ['Strength', 'Anticipation', 'Composure', 'Composure', 'Jumping', 'WorkRate', 'Bravery', 'Balance', 'Teamwork', 'Determination', 'Concentration', 'Aggression', 'Decisions'], 
	'ClearingAbility'		: ['Anticipation', 'Composure', 'Technique', 'Teamwork', 'Determination', 'Concentration', 'Heading', 'Decisions']
}




######################################################################################################
######################################################################################################
############	  PIPELINE METHODS
######################################################################################################
######################################################################################################
def get_monthly_wage(row):
	# Estimates monthly wage from weekly wage (avilable in csv)
	return round((float(row['Weeklywage'])/7)*30, 2) 


def get_clubUID(row):
	clubs_df 	=	pd.read_csv('csv/clubs.csv', sep=';', encoding='utf-8')
	try:
		return clubs_df.query('Name == "{}"'.format(row['Club'])).iloc[0]['ClubUID']
	except:
		return '-'

def get_rating(row, attrs):
	#	Receives attrs list and assign to column the average value of all of them.
	rating = 0
	for at in attrs:
		rating += row[at]
	return round(rating/len(attrs), 3)

def pipeline(input_csv, output_csv):
	stages = [
		{'rating_name':'PrimaryRating', 'attrs':primary_attrs},
		{'rating_name':'BackgroundRating', 'attrs':background_attrs},

		{'rating_name':'TechnicalRating', 'attrs':technical_attrs},
		{'rating_name':'MentalRating', 'attrs':mental_attrs},
		{'rating_name':'PhysicalRating', 'attrs':physical_attrs},
		{'rating_name':'GoalkeeperRating', 'attrs':goalkeeper_attrs},

	]
	df = pd.read_csv(input_csv, sep=';')
	# for ab in abilities_dict.keys():
	# 	df[ab] = df.apply(get_rating, args=(abilities_dict[ab], ), axis=1)		
	df.apply(get_monthly_wage, axis=1)
	df.to_csv(output_csv, sep=';')
