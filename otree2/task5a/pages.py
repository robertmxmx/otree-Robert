from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Participant1(Page):
    form_model = 'group'

    def get_form_fields(self):
        if self.player.id_in_group == 1:
            return ['p1_sent']

    def p1_sent_choices(self):
        if self.player.id_in_group == 1:    # determine how much participant 1 can send
            choices = [0]
            while choices[-1] != Constants.initial_points:
                choices.append(choices[-1] + 0.5)
            return choices

    def is_displayed(self):
        return self.player.id_in_group == 1

    def vars_for_template(self):
        return {
            'round_number': self.round_number
        }

    def before_next_page(self):
        if self.round_number == 1:  # reset payoffs on first round
            for p in self.group.get_players():
                p.participant.payoff = c(Constants.initial_payoff)


class ProcessingPage(WaitPage):
    pass


class Participant2(Page):
    form_model = 'group'

    def get_form_fields(self):
        if self.player.id_in_group == 2:
            return ['p2_sent']

    def p2_sent_choices(self):
        if self.player.id_in_group == 2:
            choices = [0]
            while choices[-1] != (self.group.p1_sent*Constants.multiplier):
                choices.append(choices[-1] + 0.5)
            return choices

    def is_displayed(self):
        return self.player.id_in_group == 2

    def vars_for_template(self):
        return {
            'round_number': self.round_number,
            'p2_payoff': self.group.p1_sent * Constants.multiplier,
        }


class ProcessingPage2(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_payoffs()


class Outcome(Page):

    def vars_for_template(self):
        return {
            'round_number': self.round_number,
            'p1_sent': self.group.p1_sent,
            'p2_sent': self.group.p2_sent,
            'p2_payoff': self.group.p1_sent*Constants.multiplier,
            'payoff': self.player.payoff
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
            'total_earnings': self.player.participant.payoff
        }

    def before_next_page(self):
        if 'summary_data' in self.participant.vars:
            self.participant.vars['summary_data'].append(('Task 5', self.participant.payoff))


page_sequence = [
    Participant1,
    ProcessingPage,
    Participant2,
    ProcessingPage2,
    Outcome,

    Survey,
    End,
]