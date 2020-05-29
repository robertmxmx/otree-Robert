from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class ParticipantADecision(Page):
    form_model = 'group'
    form_fields = ['a_decision']

    def is_displayed(self):
        return self.participant.id_in_session % 2


class ParticipantBDecision(Page):
    form_model = 'group'
    form_fields = ['b_decision1', 'b_decision2', 'b_decision3', 'b_decision4', 'b_decision5', 'b_decision6',
                   'b_decision7', 'b_decision8', 'b_decision9', 'b_decision10', 'b_decision11']

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
                Participant A proposed the following allocation:
            </p>
            <ul>
                <li>Participant A: %s</li>
                <li>Participant B: %s</li>
            </ul>
            <p>
                Participant B %s this proposal
            </p>
            <p>
                Your earnings are therefore: %s
            </p>
        """ % (c(Constants.total_points - self.group.a_decision), c(self.group.a_decision),
               "accepted" if self.player.task_payoff != c(0) else "rejected", self.player.task_payoff.to_real_world_currency(self.session))
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
