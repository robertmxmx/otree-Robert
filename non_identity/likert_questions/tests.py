from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):

    def play_round(self):
        yield (pages.Main, {
            'q1': 3,
            'q2': 3,
            'q3': 3,
            'q4': 3,
            'q5': 3,
            'q6': 3,
            'q7': 3,
            'q8': 3,
            'q9': 3,
        })
