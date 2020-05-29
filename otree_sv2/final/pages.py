from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Final(Page):

    def vars_for_template(self):
        self.player.set_payoff()
        return {
            'payoff': self.participant.payoff.to_real_world_currency(self.session)
        }


page_sequence = [
    Final,
]
