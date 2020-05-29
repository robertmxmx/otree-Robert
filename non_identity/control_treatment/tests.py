from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
from otree.api import Submission


class PlayerBot(Bot):

    def play_round(self):
        yield Submission(pages.Task1Instructions, check_html=False)
        yield (pages.Task1Comprehension, {
            't1_c1_1': 10,
            't1_c1_2': 10,
            't1_c2_1': 12,
            't1_c2_2': 2
        })
        yield (pages.Task1, {'t1_option': 1})
