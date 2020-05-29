from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):

    def play_round(self):
        yield (pages.Main, {
            'q1': 'Male',
            'q2': 'Law',
            'q3': 'Antarctica',
            'q4': 5,
            'q5': 'Buddhism'
        })
