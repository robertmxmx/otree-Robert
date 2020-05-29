from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import csv, random


author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'statement_task'
    players_per_group = None
    num_rounds = 1

    agree_questions1 = '_agree_questions1.csv'
    agree_questions2 = '_agree_questions2.csv'


class Subsession(BaseSubsession):
    def creating_session(self):
        # Read questions and answers for Group 1
        with open(Constants.agree_questions1, 'r') as f:
            csv_f = list(csv.reader(f))
            self.session.vars['agree_questions1'] = csv_f.copy()

        # Read questions and answers for Group 2
        with open(Constants.agree_questions2, 'r') as f:
            csv_f = list(csv.reader(f))
            self.session.vars['agree_questions2'] = csv_f.copy()

        # Set statement group for each player (0 uses agree_questions1 and 1 uses agree_questions2)
        for p in self.get_players():
            if p.participant.id_in_session % 2 == 1:
                p.statement_group = 0
            else:
                p.statement_group = 1


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    statement_group = models.IntegerField()
    num_agree = models.IntegerField()
