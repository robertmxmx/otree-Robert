from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

class End(Page):

    def vars_for_template(self):
        chosen_task = self.subsession.chosen_task
        task2_payoff = c(self.participant.vars['task2_payoffs'][chosen_task-1])
        bonus = c(self.participant.vars['bonus']) if 'bonus' in self.participant.vars else None
        self.participant.payoff = c(task2_payoff + bonus) if bonus is not None else c(task2_payoff)

        return {
            'chosen_task': chosen_task,
            'participation_fee': self.session.config['participation_fee'],
            'task2_payoff': task2_payoff.to_real_world_currency(self.session),
            'bonus': bonus.to_real_world_currency(self.session) if bonus is not None else None
        }

page_sequence = [
    End
]
