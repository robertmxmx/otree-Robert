from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):

    def play_round(self):
        yield (pages.Intro)
        yield (pages.Instructions)
        yield (pages.DInstructions)
        yield (pages.DInstructions2)

        if self.session.config['treatment'] == 1:
            yield (pages.Comprehension, Constants.correct_vals_pun)
        elif self.session.config['treatment'] == 2:
            yield (pages.Comprehension, Constants.correct_vals_noPun)