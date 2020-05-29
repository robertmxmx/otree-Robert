from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Survey(Page):
    form_model = 'player'
    form_fields = ['money_q1', 'money_q2', 'money_q3', 'money_q4', 'money_q5', 'money_q6', 'money_q7', 'money_q8',
                   'money_q9', 'money_q10', 'money_q11', 'sex', 'age', 'areaOfStudy', 'numExperiments', 'religion',
                   'countryOfBirth', 'yearsInAus', 'exp_ques1']


page_sequence = [
    Survey
]
