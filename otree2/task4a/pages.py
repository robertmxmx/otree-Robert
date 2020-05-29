from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Role1(Page):
    form_model = 'group'
    form_fields = ['r1_action']

    def is_displayed(self):
        return self.player.id_in_group == 1

    def vars_for_template(self):
        return {
            'round_number': self.round_number
        }

    def before_next_page(self):
        if self.round_number == 1:
            for p in self.group.get_players():
                p.participant.payoff = c(Constants.initial_payoff)


class ProcessingPage(WaitPage):
    pass


class Role2(Page):
    form_model = 'group'

    def is_displayed(self):
        return self.player.id_in_group == 2

    def get_form_fields(self):
        if self.group.r1_action == "CHALLENGE":
            return ['r2_action']
        else:
            return []

    def vars_for_template(self):
        return {
            'round_number': self.round_number,
            'r1_action': self.group.r1_action
        }


class ProcessingPage2(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_payoffs()


class Outcome(Page):

    def vars_for_template(self):
        return {
            'round_number': self.round_number,
            'r1_action': self.group.r1_action,
            'r2_action': self.group.r2_action,
            'payoff': self.player.payoff,
            'final_payoff': self.participant.payoff
        }


class Survey(Page):
    form_model = 'player'
    form_fields = ['survey_q1', 'survey_q2']

    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):
        return {
            'id': self.player.id_in_group
        }


class End(Page):

    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):
        return {
            'total_earnings': self.participant.payoff
        }

    def before_next_page(self):
        if 'summary_data' in self.participant.vars:
            self.participant.vars['summary_data'].append(('Task 4', self.participant.payoff))


page_sequence = [
    Role1,
    ProcessingPage,
    Role2,
    ProcessingPage2,

    Outcome,

    Survey,
    End
]