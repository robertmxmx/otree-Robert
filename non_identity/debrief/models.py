from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'debrief'
    players_per_group = None
    num_rounds = 1

    venue_info_file = '_venue_info.csv'


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    def to_c(self, value):
        return c(value).to_real_world_currency(self.session)
