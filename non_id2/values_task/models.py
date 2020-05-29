from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


class Constants(BaseConstants):
    name_in_url = 'values_task'
    players_per_group = None
    num_rounds = 1

    question_labels = [
        '''I always want more.''',
        '''Actually, I am kind of greedy.''',
        '''One can never have too much money.''',
        '''As soon as I have acquired something, I start to think about the next thing I want.''',
        '''It doesn't matter how much I have. I am never completely satisfied.''',
        '''My life motto is "more is better".''',
        '''I can't imagine having too many things.'''
    ]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


def create_field():
    for q_label in Constants.question_labels:
        yield models.StringField(
            label=q_label,
            choices=['Strongly Disagree', 'Disagree', 'Neither Agree Nor Disagree',
                     'Agree', 'Strongly Agree'],
            widget=widgets.RadioSelect
        )


next_q = create_field()


class Player(BasePlayer):
    q1 = next(next_q)
    q2 = next(next_q)
    q3 = next(next_q)
    q4 = next(next_q)
    q5 = next(next_q)
    q6 = next(next_q)
    q7 = next(next_q)
