from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Instructions(Page):
    pass


class Comprehension(Page):
    form_model = 'player'
    form_fields = ['comp1a', 'comp1b', 'comp1c', 'comp2a', 'comp2b', 'comp2c', 'comp3']

    def error_message(self, values):
        errors = []
        cv = Constants.comp_answers

        if values['comp1a'] != cv['comp1a'] or values['comp1b'] != cv['comp1b'] or values['comp1c'] != cv['comp1c']:
            self.player.comp1_wrong += 1
            errors.append("Question 1 is incorrect")
        if values['comp2a'] != cv['comp2a'] or values['comp2b'] != cv['comp2b'] or values['comp2c'] != cv['comp2c']:
            self.player.comp2_wrong += 1
            errors.append("Question 2 is incorrect")
        if values['comp3'] != cv['comp3']:
            self.player.comp3_wrong += 1
            errors.append("Question 3 is incorrect")

        return errors


class Choice(Page):
    form_model = 'player'
    form_fields = ['option']

    def before_next_page(self):
        self.player.set_payoffs()


class Summary(Page):
    pass


class WaitEnd(WaitPage):
    wait_for_all_groups = True


page_sequence = [
    Instructions,
    Comprehension,
    Choice,
    Summary,

    WaitEnd,
]
