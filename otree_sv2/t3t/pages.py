from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class ParticipantADecision(Page):
    form_model = 'group'
    form_fields = ['a_transfer']

    def is_displayed(self):
        return self.participant.id_in_session % 2


class ParticipantBDecision(Page):
    form_model = 'group'
    form_fields = ['b_transfer1', 'b_transfer2', 'b_transfer3', 'b_transfer4']

    def is_displayed(self):
        return not self.participant.id_in_session % 2


class ProcessingPage(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_payoffs()


class Outcome(Page):

    def before_next_page(self):
        self.participant.vars['task_outcomes'].append("""
            <h5>
                Task 3 Earnings
            </h5>
            <p>
                Participant A chose to send %s
            </p>
            <p>
                Participant B therefore received %s
            </p>
            <p>
                Participant B chose to send %s back to Participant A
            </p>
            <p>
                Your earnings are therefore: %s
            </p>
        """ % (c(self.group.a_transfer), c(3*self.group.a_transfer), self.group.b_transfer,
               self.player.task_payoff.to_real_world_currency(self.session))
        )


class Survey(Page):
    form_model = 'player'

    def get_form_fields(self):
        if self.participant.id_in_session % 2:
            return ['survey_qa1']
        else:
            return ['survey_qb1']

    def vars_for_template(self):
        return {
            'check_participant_a': self.participant.id_in_session % 2,
        }


page_sequence = [
    ParticipantADecision,
    ParticipantBDecision,
    ProcessingPage,
    Outcome,
    Survey,
]
