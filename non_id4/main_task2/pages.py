from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class AInstructions(Page):
    pass


class AComprehension(Page):
    form_model = 'player'
    form_fields = ['a_comp1', 'a_comp2', 'a_comp3']

    def error_message(self, values):
        errs = []
        cv = Constants.a_comp_answers

        if values['a_comp1'] != cv['a_comp1']:
            self.player.a_comp1_wrong += 1
            errs.append("Question 1 is incorrect")
        if values['a_comp2'] != cv['a_comp2']:
            self.player.a_comp2_wrong += 1
            errs.append("Question 2 is incorrect")
        if values['a_comp3'] != cv['a_comp3']:
            self.player.a_comp3_wrong += 1
            errs.append("Question 3 is incorrect")

        return errs


class AChoice(Page):
    form_model = 'player'
    form_fields = ['a_option', 'a_revealed']


class ARevealed(Page):
    form_model = 'player'
    form_fields = ['a_option']

    def is_displayed(self):
        return self.player.a_revealed


class AWaitEnd(WaitPage):

    def after_all_players_arrive(self):
        for p in self.group.get_players():
            p.set_a_payoffs()


class BInstructions(Page):
    pass


class BComprehension(Page):
    form_model = 'player'
    form_fields = ['b_comp1a', 'b_comp1b', 'b_comp2a', 'b_comp2b']

    def error_message(self, values):
        errs = []
        cv = Constants.b_comp_answers

        if values['b_comp1a'] != cv['b_comp1a'] or values['b_comp1b'] != cv['b_comp1b']:
            self.player.b_comp1_wrong += 1
            errs.append("Question 1 is incorrect")
        if values['b_comp2a'] != cv['b_comp2a'] or values['b_comp2b'] != cv['b_comp2b']:
            self.player.b_comp2_wrong += 1
            errs.append("Question 2 is incorrect")

        return errs


class BChoice(Page):
    form_model = 'player'
    form_fields = ['b_option']

    def before_next_page(self):
        self.player.set_b_payoffs()


class CInstructions(Page):
    pass


class CComprehension(Page):
    form_model = 'player'
    form_fields = ['c_comp1a', 'c_comp1b', 'c_comp2a', 'c_comp2b']

    def error_message(self, values):
        errs = []
        cv = Constants.c_comp_answers

        if values['c_comp1a'] != cv['c_comp1a'] or values['c_comp1b'] != cv['c_comp1b']:
            self.player.c_comp1_wrong += 1
            errs.append("Question 1 is incorrect")
        if values['c_comp2a'] != cv['c_comp2a'] or values['c_comp2b'] != cv['c_comp2b']:
            self.player.c_comp2_wrong += 1
            errs.append("Question 2 is incorrect")

        return errs


class CChoice(Page):
    form_model = 'player'
    form_fields = ['c_option']

    def before_next_page(self):
        self.player.set_c_payoffs()


class WaitEnd(WaitPage):

    def after_all_players_arrive(self):
        for p in self.group.get_players():
            p.finalize()


page_sequence = [
    AInstructions,
    AComprehension,
    AChoice,
    ARevealed,
    AWaitEnd,

    BInstructions,
    BComprehension,
    BChoice,

    CInstructions,
    CComprehension,
    CChoice,

    WaitEnd,
]
