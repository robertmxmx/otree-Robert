from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import math


class Main(Page):

    def vars_for_template(self):
        return {
                'payoff_without_show_up_fee': self.participant.payoff.to_real_world_currency(self.session),
                'rounded_total': math.ceil(self.participant.payoff_plus_participation_fee())
                }


page_sequence = [Main]
