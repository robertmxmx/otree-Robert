from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

class Welcome(Page):
    def vars_for_template(self):
        return {
            'aud_per_point': c(1).to_real_world_currency(self.session)
        }

class InternetRequirement(Page):
    pass


page_sequence = [
    Welcome,
    InternetRequirement
]
