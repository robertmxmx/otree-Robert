from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Survey(Page):
    form_model = 'player'
    form_fields = ['sex', 'age', 'areaOfStudy', 'numExperiments', 'religion', 'country',
                   'exp_ques1', 'exp_ques2', 'exp_ques3']


page_sequence = [
    Survey
]
