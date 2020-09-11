from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

def get_vars(s):
    chosen_task = s.subsession.chosen_task
    task2_payoff = c(s.participant.vars['task2_payoffs'][chosen_task-1])
    task1_payoff = c(Constants.task1_payoff_AUD / s.session.config['real_world_currency_per_point'])
    s.participant.payoff = c(task2_payoff + task1_payoff)

    return {
        'chosen_task': 'a' if chosen_task == 1 else 'b',
        'participation_fee': s.session.config['participation_fee'],
        'task1_payoff': task1_payoff.to_real_world_currency(s.session),
        'task2_payoff': task2_payoff.to_real_world_currency(s.session)
    }

class WithoutID(Page):
    form_model = 'player'
    form_fields = [ 'pay_id' ]

    def vars_for_template(self):
        return get_vars(self)

class WithID(Page):

    def vars_for_template(self):
        return get_vars(self)

page_sequence = [
    WithoutID,
    WithID
]
