from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):

    def play_round(self):
        yield (pages.Survey, {'money_q1': 1, 'money_q2': 1, 'money_q3': 1, 'money_q4': 1, 'money_q5': 1, 'money_q6': 1,
                              'money_q7': 1, 'money_q8': 1, 'money_q9': 1, 'money_q10': 1, 'money_q11': 1,
                              'sex': 'Male', 'age': 1, 'areaOfStudy': 'Engineering', 'numExperiments': 1,
                              'religion': 'Christian', 'countryOfBirth': 1, 'yearsInAus': 1, 'exp_ques1': 1})
