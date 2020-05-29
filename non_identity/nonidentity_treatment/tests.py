from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
from otree.api import Submission


class PlayerBot(Bot):

    def play_round(self):
        yield Submission(pages.Task1Instructions, check_html=False)
        yield (pages.Task1Comprehension, {
            't1_c1_1': 12,
            't1_c1_2': 0,
            't1_c1_3': 2,
            't1_c2_1': 10,
            't1_c2_2': 10,
            't1_c2_3': 0,
            't1_c3': 2
        })
        yield (pages.Task1, {'t1_option': 1})

        yield Submission(pages.Task2aInstructions, check_html=False)
        yield (pages.Task2aComprehension, {
            't2a_c1': 2,
            't2a_c2': 3,
            't2a_c3': 1,
        })
        yield (pages.Task2a, {'t2a_option': 1})

        yield Submission(pages.Task2bInstructions, check_html=False)
        yield (pages.Task2bComprehension, {
            't2b_c1_1': 12,
            't2b_c1_2': 2,
            't2b_c2_1': 10,
            't2b_c2_2': 10,
        })
        yield (pages.Task2b, {'t2b_option': 1})

        yield Submission(pages.Task2cInstructions, check_html=False)
        yield (pages.Task2cComprehension, {
            't2c_c1_1': 12,
            't2c_c1_2': 10,
            't2c_c2_1': 10,
            't2c_c2_2': 2,
        })
        yield (pages.Task2c, {'t2c_option': 1})
