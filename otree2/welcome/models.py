from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random

class Constants(BaseConstants):
    name_in_url = 'welcome'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):

    def creating_session(self):
        self.session.vars['group_mat'] = []
        for p in self.get_players():
            p.participant.vars['summary_data'] = []


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass
