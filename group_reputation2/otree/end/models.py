from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random


class Constants(BaseConstants):
    name_in_url = 'end'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    chosen_task = models.IntegerField(initial=random.randint(1, 2))


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass
