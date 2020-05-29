from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import random


class Main(Page):
    form_model = 'player'
    form_fields = ['num_agree']

    def vars_for_template(self):
        if self.player.statement_group == 1:
            statements = Constants.neutral_statements.copy()
        else:
            statements = Constants.neutral_statements.copy() + Constants.test_statements.copy()

        random.shuffle(statements)

        return {
            'statements': statements
        }

    def num_agree_error_message(self, value):
        if self.player.statement_group == 1:
            statements_size = len(Constants.neutral_statements)
        else:
            statements_size = len(Constants.neutral_statements + Constants.test_statements)

        if not 0 <= value <= statements_size:
            return 'Value must be between 0 and ' + str(statements_size)


page_sequence = [
    Main
]
