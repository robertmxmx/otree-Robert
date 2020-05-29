from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):

    def play_round(self):
        yield (pages.Start)
        yield (pages.Stage1Instructions)
        yield (pages.Stage2Instructions)
        yield (pages.Stage3Instructions)
        yield (pages.ComprehensionQuestions, {'c1': 1, 'c2': 1, 'c3': 1, 'c4': 1, 'c5': 4})
