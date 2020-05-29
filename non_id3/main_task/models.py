from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random


class Constants(BaseConstants):
    name_in_url = 'main_task'
    players_per_group = None
    num_rounds = 1

    instructions = 'main_task/InstructionsContent.html'


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


def create_field():
    # creates the fields that use the 7-point likert scale
    return models.StringField(
        choices=['Strongly Disagree', 'Disagree', 'Somewhat Disagree', 'Neither Agree Nor Disagree',
                 'Somewhat Agree', 'Agree', 'Strongly Agree'],
        widget=widgets.RadioSelect
    )


class Player(BasePlayer):
    # Comprehension questions
    comp1a = models.IntegerField()
    comp1b = models.IntegerField()
    comp1c = models.IntegerField()
    comp2a = models.IntegerField()
    comp2b = models.IntegerField()
    comp2c = models.IntegerField()
    comp3 = models.BooleanField(choices=[[True, 'Yes'], [False, 'No']])
    comp1_wrong = models.IntegerField()     # These count how many times
    comp2_wrong = models.IntegerField()     # each comprehension question
    comp3_wrong = models.IntegerField()     # was answered incorrectly
    option = models.IntegerField(
        widget=widgets.RadioSelect,
        choices=[[1, 'Option 1'], [2, 'Option 2']]
    )
    payoffA = models.CurrencyField()
    payoffB = models.CurrencyField()
    survey_q1 = create_field()
    survey_q2 = create_field()
    survey_q3 = create_field()
    survey_q4 = create_field()

    def set_payoffs(self):                  # sets payoff for player, participant A and participant B
        if self.option == 1:
            self.payoff = c(10)
            self.payoffA = c(10)
            self.payoffB = c(0)
        else:
            self.payoff = c(12)
            self.payoffA = c(0)
            self.payoffB = c(2)
