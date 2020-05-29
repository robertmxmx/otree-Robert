from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):

    def play_round(self):
        pass
        yield (pages.Survey, {
            'sex': 'Male',
            'age': 5,
            'areaOfStudy': 'Engineering',
            'numExperiments': 0,
            'religion': 'Jewish',
            'country': 'test_input',
            'exp_ques1': 1,
            'exp_ques2': 'test_input',
            'exp_ques3': 'test_input'
        })