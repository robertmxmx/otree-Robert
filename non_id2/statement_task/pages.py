from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import random

class Main(Page):
    form_model = 'player'
    form_fields = ['num_agree']

    def vars_for_template(self):
        if self.participant.id_in_session % 2 == 1:
            statements = Constants.statements1.copy()
        else:
            statements = Constants.statements2.copy()

        random.shuffle(statements)

        return {
            'statements': statements
        }

    def num_agree_error_message(self, value):
        if self.participant.id_in_session % 2 == 1 and not 0 <= value <= len(Constants.statements1):
            return 'Value must be between 0 and ' + str(len(Constants.statements1))
        elif self.participant.id_in_session % 2 == 0 and not 0 <= value <= len(Constants.statements2):
            return 'Value must be between 0 and ' + str(len(Constants.statements2))


page_sequence = [
    Main
]
