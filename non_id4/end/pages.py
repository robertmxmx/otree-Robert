from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Main(Page):

    def vars_for_template(self):
        t1_data = self.participant.vars['t1_data']
        t2_data = self.participant.vars['t2_data']

        return {
            't1_payoff': t1_data['payoff'],
            't2_chosen_task': t2_data['chosen_task'],
            't2_payoff': t2_data['payoff'],
        }



page_sequence = [
    Main,
]
