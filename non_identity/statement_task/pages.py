from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import random


class Main(Page):
    form_model = 'player'
    form_fields = ['num_agree']

    def vars_for_template(self):
        if self.player.statement_group == 0:
            data = self.session.vars['agree_questions1'].copy()
        else:
            data = self.session.vars['agree_questions2'].copy()

        statements = [x[0] for x in data]
        random.shuffle(statements)
        num_statements = len(data)
        return {
            'num_statements': num_statements,
            'statements': statements,
            'treatment': self.session.config['treatment']
        }

    def num_agree_error_message(self, value):
        if self.participant.id_in_session % 2 == 1 and not 0 <= value <= len(self.session.vars['agree_questions1'].copy()):
            return 'Input must be between 0 and ' + str(len(self.session.vars['agree_questions1'].copy()))
        elif self.participant.id_in_session % 2 == 0 and not 0 <= value <= len(self.session.vars['agree_questions2'].copy()):
            return 'Input must be between 0 and ' + str(len(self.session.vars['agree_questions2'].copy()))


page_sequence = [Main]
