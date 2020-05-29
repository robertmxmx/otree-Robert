from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):

    def play_round(self):
        yield (pages.Main, {
            'q1': 'Male',
            'q2': 'Medicine',
            'q3': 'straya',
            'q4': 20,
            'q5': 'Buddhism',
            'q6': 2
        })
