from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Main(Page):
    form_model = 'player'
    form_fields = ['q1a', 'q1b', 'q2a', 'q2b', 'q3a', 'q3b']

    def vars_for_template(self):
        t1_data = self.participant.vars['t1_data']
        return {
            'option': t1_data['option'],
            'payoffA': t1_data['payoffA'],
            'payoffB': t1_data['payoffB'],
        }


page_sequence = [
    Main,
]