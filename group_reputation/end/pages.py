from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Main(Page):

    def vars_for_template(self):
        return {
            'participation_fee': self.session.config['participation_fee'],
            'task2_payoff': self.participant.payoff.to_real_world_currency(self.session)
        }


page_sequence = [
    Main
]
