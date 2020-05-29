from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

import task1.pages as t1_pages

class InitialWait(WaitPage):
    wait_for_all_groups = True
    after_all_players_arrive = 'reset_payoffs'

class Instructions(Page):
    pass

class Revelation(Page):
    def vars_for_template(self):
        statements = []

        for statement in Constants.reveal_statements:
            b_vars = self.group.get_player_by_role('B').participant.vars

            index = b_vars['statements'][statement] - 1

            bid = b_vars['statements_bid'][statement]
            if bid != Constants.opt_out_text:
                bid = "$" + bid

            statements.append(dict(
                label=Constants.statements[statement][index][1], 
                bid=bid
            ))

        return dict(statements=statements)

class ADecision(t1_pages.ADecision):
    pass

class BDecision(t1_pages.BDecision):
    pass

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
        

class Survey(Page):
    form_model = 'player'

    def get_form_fields(self):
        if self.player.role() == 'A':
            return ['surveyq_part_A', 'surveyq_why']
        else:
            return ['surveyq_part_B', 'surveyq_why']


page_sequence = [
    t1_pages.InitialWait,

    Instructions,
    Revelation,
    
    t1_pages.InitialPayoffs,
    ADecision,
    BDecision,
    t1_pages.FinalPayoffs,
    Outcome,

    Survey,
]
