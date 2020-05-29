from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
from otree.api import Submission, SubmissionMustFail
import random


class PlayerBot(Bot):

    def play_round(self):
        yield Submission(pages.Instructions, check_html=False)
        yield SubmissionMustFail(pages.Comprehension, {
            'comp1a': 2, 'comp1b': 2, 'comp1c': 2, 
            'comp2a': 2, 'comp2b': 2, 'comp2c': 2,
            'comp3': False
        })
        yield (pages.Comprehension, Constants.comp_answers)
        yield (pages.Choice, {'option': random.choice([1, 2])})
        yield Submission(pages.Summary, check_html=False)
