from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Main(Page):

    def vars_for_template(self):
        chosen_task = self.subsession.chosen_task
        task2_payoff = c(self.participant.vars['task2_payoffs'][chosen_task-1])
        task1_payoff = c(Constants.task1_payoff_AUD / self.session.config['real_world_currency_per_point'])
        self.participant.payoff = c(task2_payoff + task1_payoff)

        return {
            'chosen_task': 'a' if chosen_task == 1 else 'b',
            'participation_fee': self.session.config['participation_fee'],
            'task1_payoff': task1_payoff.to_real_world_currency(self.session),
            'task2_payoff': task2_payoff.to_real_world_currency(self.session)
        }


page_sequence = [
    Main
]
