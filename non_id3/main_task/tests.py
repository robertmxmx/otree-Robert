from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
from otree.api import Submission, SubmissionMustFail
import random


class PlayerBot(Bot):

    def play_round(self):
        yield Submission(pages.Instructions, check_html=False)
        yield (pages.Comprehension, {
            'comp1a': 12, 'comp1b': 0, 'comp1c': 2,
            'comp2a': 10, 'comp2b': 10, 'comp2c': 0,
            'comp3': True
        })
        yield (pages.Choice, {'option': random.choice([1, 2])})
        yield (pages.Summary)
        yield Submission(pages.Intermission, check_html=False)
        yield (pages.Survey, {
            'survey_q1': 'Strongly Disagree',
            'survey_q2': 'Disagree',
            'survey_q3': 'Strongly Agree',
            'survey_q4': 'Agree'
        })
