from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Hold(Page):

    def is_displayed(self):
        if self.subsession.get_task_number() == 1:
            return False
        else:
            return True


class Start(Page):

    def vars_for_template(self):
        return {'task_number': self.subsession.get_task_number()}


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
        errs = []
        cv = Constants.comp_answers

        if values['c1'] != cv['c1']:
            self.player.c1wrong += 1
            errs.append("Question 1 is incorrect")
        if values['c2'] != cv['c2']:
            self.player.c2wrong += 1
            errs.append("Question 2 is incorrect")
        if values['c3'] != cv['c3']:
            self.player.c3wrong += 1
            errs.append("Question 3 is incorrect")
        if values['c4'] != cv['c4']:
            self.player.c4wrong += 1
            errs.append("Question 4 is incorrect")
        if values['c5'] != cv['c5']:
            self.player.c5wrong += 1
            errs.append("Question 5 is incorrect")

        return errs


page_sequence = [
    Hold,

    Start,
    Stage1Instructions,
    Stage2Instructions,
    Stage3Instructions,
    ComprehensionQuestions
]
