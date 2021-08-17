import pipeline
'''
Puede ser útil a la hora de renderizar la página de jugador o de plantilla, no así para mostrar resultados de búsqueda u otra
tarea que requiera obtener muchos jugadores, en cuyo caso es preferible emplear los resultados del dataframe (lista de dicts)
'''

class Player():
    #   Players from my squad

    reg = None # reg from dataframe (csv row)
    
    # Player basic information
    basic_info = {
        'UID':'',
        'Name':'',
        'Age':'',
        'Club':'',
        'Value':'',
        'Face':'',  # face path    
    }
    #   Contract information
    contract = {
        'EndOfContract':None, #date
        'WeeklyWage':None,   #int
    }

    #   Positions
    positions = ''  #str format
    positons_list = []#split(',')
    positions_rating = {}
    position_group = ''     #   General position group (GK, DF, MED, ATT)

    #   Attributes groups (dicts attr:value)
    technical = {}
    mental = {}
    physical = {}
    goalkeeper = {}

    background = {}
    primary = {}

    hidden = {}
    person = {}  

    roles_rating = {}
    abilities_rating = {}

    #   Ratings (attrs groups average)
    ratings = {
        'TechnicalRating':'',
        'MentalRating':'',
        'PhysicalRating':'',
        'GoalkeeperRating':'',

        'BackgroundRating':'',
        'PrimaryRating':'',
    }

    # Custom ratings
    custom_ratings = []



    def __init__(self, reg):
        #   reg: register from players dataframe
        # print(dict(reg))
        
        self.reg = reg
        #   Filling basic_info
        for field in list(self.basic_info.keys())[:-1]:
            self.basic_info[field]  =   reg[field]   
        #   Filling contract info
        self.contract['EndOfContract'] = reg.EndOfContract
        self.contract['WeeklyWage'] = reg.WeeklyWage
        #   Filling positions info
        self.positions = reg.Positions
        self.positions_list = reg.Positions.split(',')
        for position in pipeline.positions:
            if int(reg[position]) >= 10:
                self.positions_rating[position] = reg[position]

        #   Technical
        for ta in pipeline.attrs_average_dict[list(pipeline.attrs_average_dict.keys())[0]]:
            self.technical[ta] = reg[ta]
        #   Mental
        for ta in pipeline.attrs_average_dict[list(pipeline.attrs_average_dict.keys())[1]]:
            self.mental[ta] = reg[ta]

        #   Physical
        for ta in pipeline.attrs_average_dict[list(pipeline.attrs_average_dict.keys())[2]]:
            self.physical[ta] = reg[ta]

        #   Goalkeeper
        for ta in pipeline.attrs_average_dict[list(pipeline.attrs_average_dict.keys())[3]]:
            self.goalkeeper[ta] = reg[ta]

        self.attrs = {**self.technical, **self.mental, **self.physical}

        #   Background
        for ta in pipeline.attrs_average_dict[list(pipeline.attrs_average_dict.keys())[4]]:
            self.background[ta] = reg[ta]
    
        #   Primary
        for ta in pipeline.attrs_average_dict[list(pipeline.attrs_average_dict.keys())[5]]:
            self.primary[ta] = reg[ta]

        #   Hidden
        for ta in pipeline.hidden_attrs:
            self.hidden[ta] = reg[ta]
        #   Person
        for ta in pipeline.person_attrs:
            self.person[ta] = reg[ta]

        #   Roles
        for ta in list(pipeline.roles_dict.keys()):
            self.roles_rating[ta] = reg[ta]
        #   Abilities
        for ta in list(pipeline.abilities_dict.keys()):
            self.abilities_rating[ta] = reg[ta]

        #   Ratings
        self.ratings['TechnicalRating'] = reg.TechnicalRating
        self.ratings['MentalRating'] = reg.MentalRating
        self.ratings['PhysicalRating'] = reg.PhysicalRating
        self.ratings['GoalkeeperRating'] = reg.GoalkeeperRating
        self.ratings['BackgroundRating'] = reg.BackgroundRating
        self.ratings['PrimaryRating'] = reg.PrimaryRating
        

        # Custom ratings
    

    def delete_from_preselection():
        pass

    def add_custom_rating(attrs):
        #   attrs: list with considered attributes or dict indicating weights for attrs (weights must sum 1).
        # self.custom_ratings.append(...)
        pass


    def print_player(self):
        pass