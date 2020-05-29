from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random

"""
A portion of the following code has been used from:
Title:          otree_rets Source Code
Author:         Kephart, C
Date:           2017
Available at:   https://github.com/EconomiCurtis/otree_rets
"""


class Constants(BaseConstants):
    name_in_url = 'ret'
    players_per_group = 8
    num_rounds = 90

    reference_texts = [
        'uIzR',
        'dWg5',
        '6kdA',
        'zflY',
        'CwNg',
        'GJcR',
        '1MUj',
        'GleS',
        '4gKx',
        'CdsT',
        'Mf4U',
        'sUhJ',
        '1Ltw',
        '2mrm',
        'f5UI',
        'hNqN',
        '2Pqv',
        'vLuq',
        'IYYP',
        'M9X6',
        'qflm',
        '7PaW',
        'YB4F',
        '2NFP',
        'h6QM',
        'xLkH',
        'izif',
        'r7Ml',
        'ERJ8',
        'geTe',
        'L15N',
        'uTKl',
        'wRuQ',
        'MFNc',
        'YS4B',
        'syXc',
        'QgvI',
        'a5bk',
        'MqCQ',
        'NzsZ',
        '1maT',
        'mN28',
        'BJet',
        'xBhz',
        'rkn7',
        '5r3d',
        'pYQD',
        'Rkn1',
        'FJIv',
        'pZMh',
        '3V4w',
        'zWtd',
        'ArfP',
        'IdzS',
        'mC9T',
        '7cIv',
        'TjcG',
        'fZ15',
        'NlsB',
        'tPX4',
        'HLTg',
        'de14',
        'MbqN',
        'xywd',
        'Z3Vz',
        'XS7V',
        'ErGB',
        'HlTl',
        '9Dmt',
        'LCwT',
        'y97e',
        '6PTp',
        'vCVC',
        'MG3S',
        'kzpF',
        'WSx7IJ8YMeAF',
        '6gt6k1dZfDdL',
        '8gkmGZY36lBI',
        'tz4hJ6NVBPBq',
        'FAojzXfsCvsc',
        'Lk5bKpQ13kTv',
        'bRsi7Cbd4gPs',
        'e3Hs759fdegV',
        'NMtMkEyyyly3',
        'EJB4YDNxKcQV',
        'GSyitZNp3aCa',
        'fZPnL4W4Rk8U',
        'BXVXpjlFuIl6',
        'Bv4jsM4PphLB',
        '3wdvp9cQMEKU',
    ]


class Subsession(BaseSubsession):

    def creating_session(self):
        for p in self.get_players():
            p.correct_text = Constants.reference_texts[self.round_number - 1]


class Group(BaseGroup):

    # used to determine which color and town players initially start in
    def assign_players(self):
        num_red = 0
        num_blue = 0

        # assign color and town for top ret scorers
        for p in self.get_players():
            if p.top_scorer:
                color = p.start_color

                p.participant.vars['town'] = color
                p.participant.vars['color'] = color

                if color == 'red':
                    num_red += 1
                elif color == 'blue':
                    num_blue += 1
                else:
                    print("error: invalid start_color")

        # assign color and town for others
        for p in self.get_players():
            if 'color' not in p.participant.vars:
                color = random.choice(['red', 'blue'])

                # ensures that there are equal numbers in both towns
                if color == 'red' and num_red == int(len(self.get_players()) / 2):
                    color = 'blue'
                elif color == 'blue' and num_blue == int(len(self.get_players()) / 2):
                    color = 'red'

                p.participant.vars['town'] = color
                p.participant.vars['color'] = color

                if color == 'red':
                    num_red += 1
                elif color == 'blue':
                    num_blue += 1
                else:
                    print("error: invalid color")


class Player(BasePlayer):
    start_color = models.StringField(
        label='Which color do you wish to be assigned?',
        choices=['red', 'blue'],
        widget=widgets.RadioSelect,
    )
    correct_text = models.StringField()
    user_text = models.StringField()
    is_correct = models.BooleanField()
    top_scorer = models.BooleanField()

    def score_round(self):
        if self.user_text == self.correct_text:
            self.is_correct = True
            self.payoff += c(1)
        else:
            self.is_correct = False
