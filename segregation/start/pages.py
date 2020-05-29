from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Intro(Page):
    pass


class Instructions(Page):
    pass


class DInstructions(Page):
    pass


class DInstructions2(Page):
    pass


class Comprehension(Page):
    form_model = "player"

    def get_form_fields(self):
        if self.session.config['treatment'] == 1:
            return ['c1', 'c2', 'c3', 'c4', 'c5', 'c6a', 'c6b']
        elif self.session.config['treatment'] == 2:
            return ['c1', 'c2', 'c3', 'c4', 'c5']
        else:
            print("error: invalid treatment")

    def error_message(self, values):
        errs = []

        if self.session.config['treatment'] == 1:
            cv = Constants.correct_vals_pun
        elif self.session.config['treatment'] == 2:
            cv = Constants.correct_vals_noPun
        else:
            print("incorrect treatment given")

        for key in cv:                                              # checks if values entered by user
            if values[key] != cv[key]:                              # are the same as the correct
                errs.append("Question %s is incorrect" % key[1:])   # values (correct_vals)

        return errs


page_sequence = [
    Intro,
    Instructions,
    DInstructions,
    DInstructions2,
    Comprehension
]
