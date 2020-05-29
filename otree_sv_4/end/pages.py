from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import random
from constants import statements

class SetPayoffs(WaitPage):
    after_all_players_arrive = 'set_payoffs'

class Payment(Page):
    
    def vars_for_template(self):
        paid_task = self.subsession.paid_task

        if paid_task == 1 or paid_task == 3:    
            return self.participant.vars['task%d_vars' % paid_task]
        else:
            statement = self.subsession.chosen_statement

            statement_chosen = self.participant.vars['statements'][statement] - 1

            bid = self.participant.vars['statements_bid'][statement]
            if bid != Constants.opt_out_text:
                bid = "$" + bid

            return dict(
                statement_label=statements[statement][statement_chosen][1],
                statement_bid=bid,
            )



page_sequence = [SetPayoffs, Payment]
