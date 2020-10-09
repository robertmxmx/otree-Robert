from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random


class Constants(BaseConstants):
    name_in_url = 'end'
    players_per_group = None
    num_rounds = 1

    task1_payoff_AUD = 3


class Subsession(BaseSubsession):
    chosen_task = models.IntegerField(initial=random.randint(1, 2))


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pay_id = models.StringField(
        label="Please enter your PayID here and click Submit")
