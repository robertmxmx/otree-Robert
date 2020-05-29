from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Instructions(Page):

    def vars_for_template(self):
        return {
            'this_task1': self.subsession.this_task1,
        }


class Comprehension(Page):
    form_model = 'player'
    form_fields = ['comp1', 'comp2']

    def error_message(self, values):
        error_msgs = []

        if self.subsession.this_task1:
            if values['comp1'] != "$0":
                self.player.comp1_wrong = (self.player.comp1_wrong+1 if self.player.comp1_wrong else 1)
                error_msgs.append("Question 1 is incorrect")
        else:
            if values['comp1'] != "$10":
                self.player.comp1_wrong = (self.player.comp1_wrong+1 if self.player.comp1_wrong else 1)
                error_msgs.append("Question 1 is incorrect")

        if values['comp2'] != "$10":
            self.player.comp2_wrong = (self.player.comp2_wrong+1 if self.player.comp2_wrong else 1)
            error_msgs.append("Question 2 is incorrect")

        return error_msgs

    def vars_for_template(self):
        return {
            'this_task1': self.subsession.this_task1,
        }


class Scenario(Page):

    def is_displayed(self):
        return self.round_number == 1


class ScenarioComprehension(Page):
    form_model = 'player'

    def is_displayed(self):
        return self.round_number == 1

    def get_form_fields(self):
        if self.session.config['treatment'] == 1:
            return [
                't_comp1a', 't_comp1b', 't_comp1c',
                't_comp2a', 't_comp2b', 't_comp2c',
                't_comp3'
            ]
        else:
            return [
                'c_comp1a', 'c_comp1b',
                'c_comp2a', 'c_comp2b',
            ]

    def error_message(self, values):
        error_msgs = []
        if self.session.config['treatment'] == 1:
            if values['t_comp1a'] != 12 or values['t_comp1b'] != 0 or values['t_comp1c'] != 2:
                self.player.t_comp1_wrong = (self.player.t_comp1_wrong+1 if self.player.t_comp1_wrong else 1)
                error_msgs.append("Question 1 is incorrect")

            if values['t_comp2a'] != 10 or values['t_comp2b'] != 10 or values['t_comp2c'] != 0:
                self.player.t_comp2_wrong = (self.player.t_comp2_wrong+1 if self.player.t_comp2_wrong else 1)
                error_msgs.append("Question 2 is incorrect")

            if values['t_comp3'] != "No":
                self.player.t_comp3_wrong = (self.player.t_comp3_wrong+1 if self.player.t_comp3_wrong else 1)
                error_msgs.append("Question 3 is incorrect")
        else:
            if values['c_comp1a'] != 10 or values['c_comp1b'] != 10:
                self.player.c_comp1_wrong = (self.player.c_comp1_wrong+1 if self.player.c_comp1_wrong else 1)
                error_msgs.append("Question 1 is incorrect")

            if values['c_comp2a'] != 12 or values['c_comp2b'] != 2:
                self.player.c_comp2_wrong = (self.player.c_comp2_wrong+1 if self.player.c_comp2_wrong else 1)
                error_msgs.append("Question 2 is incorrect")

        return error_msgs


class Choice(Page):
    form_model = 'player'
    form_fields = ['option1', 'option2']

    def vars_for_template(self):
        return {
            'this_task1': self.subsession.this_task1,
        }


class SetPayoffs(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_payoffs()


page_sequence = [
    Instructions,     # todo: uncomment
    Comprehension,
    Scenario,
    ScenarioComprehension,
    Choice,
    SetPayoffs
]
