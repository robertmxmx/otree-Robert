from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):

    def play_round(self):
        yield (pages.Main, {'q1a': 1, 'q1b': 2, 'q2a': 5,
                            'q2b': 7, 'q3a': 3, 'q3b': 1})
