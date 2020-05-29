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
        self.session.vars['chosen_task'] = random.randint(1, 3)
        for p in self.get_players():
            p.participant.vars['task_payoffs'] = []
            p.participant.vars['task_outcomes'] = []



class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass
