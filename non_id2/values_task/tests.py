from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):

    def play_round(self):
        yield (pages.Main, {'q1': 'Disagree', 'q2': 'Disagree', 'q3': 'Disagree', 'q4': 'Disagree', 'q5': 'Disagree',
                            'q6': 'Disagree', 'q7': 'Disagree'})
