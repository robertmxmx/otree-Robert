from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

def get_vars(s):
    chosen_task = s.subsession.chosen_task
    task2_payoff = c(s.participant.vars['task2_payoffs'][chosen_task-1])
    s.participant.payoff = c(task2_payoff)

    return {
        'chosen_task': chosen_task,
        'participation_fee': s.session.config['participation_fee'],
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
