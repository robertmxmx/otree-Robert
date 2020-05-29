from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class End(Page):

    def vars_for_template(self):
        self.player.task1_payoff = self.participant.vars['task1_payoff']
        self.player.task2_payoff = self.participant.vars['task2_payoff']

        if self.subsession.chosen_task == 1:
            payoff = self.player.task1_payoff
        else:
            payoff = self.player.task2_payoff

        self.participant.payoff = c(round((payoff / 5) * 5))  # round to nearest 5 point

        return {
            'participation_fee': c(
                self.session.config['participation_fee'] * (1 / self.session.config['real_world_currency_per_point'])
            ),
            'final_payoff': c(
                self.participant.payoff +
                (self.session.config['participation_fee'] * (1 / self.session.config['real_world_currency_per_point']))
            ),
        }


page_sequence = [
    End,
]
