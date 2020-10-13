from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

from _myshared.uploader import get_userdata

class Constants(BaseConstants):
    name_in_url = 'start'
    players_per_group = None
    num_rounds = 1
    

class Subsession(BaseSubsession):
    def creating_session(self):
        userdata = get_userdata()
        print(userdata)


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass