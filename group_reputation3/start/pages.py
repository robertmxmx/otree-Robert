from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

class Consent(Page):
    form_model = 'player'
    form_fields = ['accept']

    def before_next_page(self):
        self.player.participant.vars['droppedout'] = not self.player.accept


class Declined(Page):
    def is_displayed(self):
        return not self.player.accept

    def app_after_this_page(self, upcoming_apps):
        if not self.player.accept:
            return upcoming_apps[-1]


class Welcome(Page):
    def vars_for_template(self):
        return {
            'aud_per_point': c(1).to_real_world_currency(self.session)
        }

class InternetRequirement(Page):
    def is_displayed(self):
        return self.session.config["online_exp"]


page_sequence = [
    Consent,
    Declined,
    Welcome,
    InternetRequirement
]
