from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Main(Page):

    def vars_for_template(self):
        return {
            'aud_per_point': c(1).to_real_world_currency(self.session)
        }


page_sequence = [
    Main
]
