from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Start(Page):

    def vars_for_template(self):
        return {
            'task_number': 1
        }


class Stage1Instructions(Page):
    pass


class Stage2Instructions(Page):
    pass


class Stage3Instructions(Page):
    pass


class ComprehensionQuestions(Page):
    form_model = 'player'
    form_fields = ['c1', 'c2', 'c3', 'c4', 'c5']

    def error_message(self, values):
        errors_arr = []
        if values['c1'] != 1:
            self.player.c1wrong += 1
            errors_arr.append('Question 1 is incorrect')
        if values['c2'] != 1:
            self.player.c2wrong += 1
            errors_arr.append('Question 2 is incorrect')
        if values['c3'] != 1:
            self.player.c3wrong += 1
            errors_arr.append('Question 3 is incorrect')
        if values['c4'] != 1:
            self.player.c4wrong += 1
            errors_arr.append('Question 4 is incorrect')
        if values['c5'] != 4:
            self.player.c5wrong += 1
            errors_arr.append('Question 5 is incorrect')
        return errors_arr


page_sequence = [
    Start,
    Stage1Instructions,
    Stage2Instructions,
    Stage3Instructions,
    ComprehensionQuestions
]
