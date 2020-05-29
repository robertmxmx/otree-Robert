from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class InitialWait(WaitPage):
    wait_for_all_groups = True

class Instructions(Page):
    pass

class Comprehension(Page):
    form_model = 'player'
    form_fields = ['c1', 'c2', 'c3', 'c4']

    def error_message(self, values):
        errors = []
        answers = Constants.comprehension_answers

        if values['c1'] != answers['c1']:
            self.player.c1wrong += 1
            errors.append("Question 1 is incorrect")

        if values['c2'] != answers['c2']:
            self.player.c2wrong += 1
            errors.append("Question 2 is incorrect")

        if values['c3'] != answers['c3']:
            self.player.c3wrong += 1
            errors.append("Question 3 is incorrect")

        if values['c4'] != answers['c4']:
            self.player.c4wrong += 1
            errors.append("Question 4 is incorrect")

        return errors

class InitialPayoffs(WaitPage):
    after_all_players_arrive = 'set_initial_payoffs'

class ADecision(Page):
    form_model = 'group'
    form_fields = ['points_taken']

    def is_displayed(self):
        return self.player.role() == 'A'

    def vars_for_template(self):
        return dict(payoffs=self.group.get_payoffs())

class BDecision(Page):
    form_model = 'group'
    form_fields = ['points_retaliated']

    def is_displayed(self):
        return self.player.role() == 'B'

    def vars_for_template(self):
        return dict(payoffs=self.group.get_payoffs())

class FinalPayoffs(WaitPage):
    after_all_players_arrive = 'set_final_payoffs'

class Outcome(Page):

    def vars_for_template(self):
        variables = dict(
            points_taken=self.group.points_taken,
            points_retaliated=self.group.points_retaliated,
            payoffs=self.group.get_payoffs(),
            final_payoff=self.player.payoff
        )

        self.participant.vars[Constants.name_in_url+'_vars'] = variables
        return variables

page_sequence = [
    InitialWait,
    InitialPayoffs,
    Instructions,
    Comprehension,
    ADecision,
    BDecision,
    FinalPayoffs,
    Outcome,
]
