from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


class Constants(BaseConstants):
    name_in_url = 'statement_task'
    players_per_group = None
    num_rounds = 1

    statements1 = [
        'This laboratory has been operating for over twenty years',
        'This research project is funded by the ARC',
        'The lead researcher of this project obtained his PhD in the USA',
        'Today’s experiment was intended to study beliefs about socially appropriate behaviour that is relevant to environmental conservation policy'
    ]
    statements2 = [
        'This laboratory has been operating for over twenty years',
        'This research project is funded by the ARC',
        'The lead researcher of this project obtained his PhD in the USA',
        'Today’s experiment was intended to study the psychological basis of behaviour that is relevant to environmental conservation policy',
        'You will be paid in task 1 the way described in the instructions'
    ]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    num_agree = models.IntegerField()
