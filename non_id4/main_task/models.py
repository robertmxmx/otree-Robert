from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random


class Constants(BaseConstants):
    name_in_url = 'main_task'
    players_per_group = None
    num_rounds = 1

    comp_answers = {
        "comp1a": 12, "comp1b": 0, "comp1c": 2,
        "comp2a": 10, "comp2b": 10, "comp2c": 0,
        "comp3a": 13, "comp3b": 3, "comp3c": 0,
        "comp4": False, "comp5": False, "comp6": 1
    }


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


def create_field():
    # creates the fields that use the 7-point likert scale
    return models.StringField(
        choices=['Strongly Disagree', 'Disagree', 'Somewhat Disagree', 'Neither Agree Nor Disagree', 'Somewhat Agree',
                 'Agree', 'Strongly Agree'], widget=widgets.RadioSelect)


class Player(BasePlayer):
    # Comprehension questions
    comp1a = models.IntegerField()
    comp1b = models.IntegerField()
    comp1c = models.IntegerField()
    comp2a = models.IntegerField()
    comp2b = models.IntegerField()
    comp2c = models.IntegerField()
    comp3a = models.IntegerField()
    comp3b = models.IntegerField()
    comp3c = models.IntegerField()
    comp4 = models.BooleanField(
        label="If you choose Option 2, then will Participant A ever be informed about this experiment?",
        widget=widgets.RadioSelectHorizontal)
    comp5 = models.BooleanField(
        label="If you choose Option 1, then will Participant B ever be informed about this experiment?",
        widget=widgets.RadioSelectHorizontal)
    comp6 = models.IntegerField(
        label="If you choose Option 3, then who will be informed about the outcome of the experiment?",
        choices=[[1, 'Participant A only'], [2, 'Participant B only'], [3, 'Both participants A and B']],
        widget=widgets.RadioSelectHorizontal)
    comp1_wrong = models.IntegerField(initial=0)  # These count how many times
    comp2_wrong = models.IntegerField(initial=0)  # each comprehension question
    comp3_wrong = models.IntegerField(initial=0)  # was answered incorrectly
    comp4_wrong = models.IntegerField(initial=0)
    comp5_wrong = models.IntegerField(initial=0)
    comp6_wrong = models.IntegerField(initial=0)
    option = models.IntegerField()
    payoffA = models.CurrencyField()
    payoffB = models.CurrencyField()
    survey_q1 = create_field()
    survey_q2 = create_field()
    survey_q3 = create_field()
    survey_q4 = create_field()

    def set_payoffs(self):  # sets payoff for player, participant A and participant B
        if self.option == 1:
            self.payoff = c(10)
            self.payoffA = c(10)
            self.payoffB = c(0)
        elif self.option == 2:
            self.payoff = c(12)
            self.payoffA = c(0)
            self.payoffB = c(2)
        else:
            self.payoff = c(13)
            self.payoffA = c(3)
            self.payoffB = c(0)

        self.participant.vars['t1_data'] = {
            'option': self.option,
            'payoff': self.payoff,
            'payoffA': self.payoffA,
            'payoffB': self.payoffB
        }
