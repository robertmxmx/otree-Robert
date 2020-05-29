from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Instructions(Page):
    pass


class Comprehension(Page):
    form_model = 'player'
    form_fields = ['comp1a', 'comp1b', 'comp1c', 'comp2a', 'comp2b', 'comp2c', 'comp3']

    def error_message(self, values):
        error_msgs = []

        if values['comp1a'] != 12 or values['comp1b'] != 0 or values['comp1c'] != 2:
            self.player.comp1_wrong = (self.player.comp1_wrong+1 if self.player.comp1_wrong else 1)
            error_msgs.append("Question 1 is incorrect")

        if values['comp2a'] != 10 or values['comp2b'] != 10 or values['comp2c'] != 0:
            self.player.comp2_wrong = (self.player.comp2_wrong+1 if self.player.comp2_wrong else 1)
            error_msgs.append("Question 2 is incorrect")

        if values['comp3'] != True:
            self.player.comp3_wrong = (self.player.comp3_wrong+1 if self.player.comp3_wrong else 1)
            error_msgs.append("Question 3 is incorrect")

        return error_msgs


class Choice(Page):
    form_model = 'player'
    form_fields = ['option']

    def before_next_page(self):
        self.player.set_payoffs()


class Summary(Page):
    pass


class Intermission(Page):
    pass


class Survey(Page):
    form_model = 'player'
    form_fields = ['survey_q1', 'survey_q2', 'survey_q3', 'survey_q4']


page_sequence = [
    Instructions,
    Comprehension,
    Choice,
    Summary,

    Intermission,
    Survey,
]
