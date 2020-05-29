from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random


class Constants(BaseConstants):
    name_in_url = 'main_task2'
    players_per_group = None
    num_rounds = 1

    a_comp_answers = {"a_comp1": 2, "a_comp2": 3, "a_comp3": True}
    b_comp_answers = {"b_comp1a": 12, "b_comp1b": 2, "b_comp2a": 10, "b_comp2b": 10}
    c_comp_answers = {"c_comp1a": 12, "c_comp1b": 10, "c_comp2a": 10, "c_comp2b": 2}

    payoffs = [
        [{'self_payoff': 10, 'other_payoff': 10}, {'self_payoff': 12, 'other_payoff': 2}],  # version 1
        [{'self_payoff': 10, 'other_payoff': 2}, {'self_payoff': 12, 'other_payoff': 10}]   # version 2
    ]


class Subsession(BaseSubsession):

    def creating_session(self):
        for p in self.get_players():
            p.chosen_task = random.choice([1, 2, 3])
            p.a_version_assigned = random.choice([1, 2])


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    chosen_task = models.IntegerField()
    #  Task 2a
    a_comp1 = models.IntegerField(label="Which option gives you the highest payoff in both versions?",
                                  widget=widgets.RadioSelectHorizontal,
                                  choices=[[1, 'Option 1'], [2, 'Option 2']])
    a_comp2 = models.IntegerField(label="If you choose option 2, then the other participant receives?",
                                  widget=widgets.RadioSelectHorizontal,
                                  choices=[[1, '$10 for sure'], [2, '$2 for sure'],
                                           [3, "Either $10 or $2 - it's a matter of chance"]])
    a_comp3 = models.BooleanField(
        label="If you click the Reveal button, will you know for sure what the other participant will receive?",
        widget=widgets.RadioSelectHorizontal)
    a_comp1_wrong = models.IntegerField(initial=0)
    a_comp2_wrong = models.IntegerField(initial=0)
    a_comp3_wrong = models.IntegerField(initial=0)
    a_version_assigned = models.IntegerField()
    a_revealed = models.BooleanField(initial=False, blank=True)
    a_option = models.IntegerField(blank=True)
    a_payoff = models.CurrencyField()
    a_other_payoff = models.CurrencyField()
    # Task 2b
    b_comp1a = models.IntegerField()
    b_comp1b = models.IntegerField()
    b_comp2a = models.IntegerField()
    b_comp2b = models.IntegerField()
    b_comp1_wrong = models.IntegerField(initial=0)
    b_comp2_wrong = models.IntegerField(initial=0)
    b_option = models.IntegerField()
    b_payoff = models.CurrencyField()
    b_other_payoff = models.CurrencyField()
    # Task 2c
    c_comp1a = models.IntegerField()
    c_comp1b = models.IntegerField()
    c_comp2a = models.IntegerField()
    c_comp2b = models.IntegerField()
    c_comp1_wrong = models.IntegerField(initial=0)
    c_comp2_wrong = models.IntegerField(initial=0)
    c_option = models.IntegerField()
    c_payoff = models.CurrencyField()
    c_other_payoff = models.CurrencyField()

    def set_a_payoffs(self):
        self.a_payoff = c(Constants.payoffs[self.a_version_assigned-1][self.a_option-1]['self_payoff'])
        self.a_other_payoff = c(Constants.payoffs[self.a_version_assigned-1][self.a_option-1]['other_payoff'])

    def set_b_payoffs(self):
        self.b_payoff = c(Constants.payoffs[0][self.b_option-1]['self_payoff'])
        self.b_other_payoff = c(Constants.payoffs[0][self.b_option-1]['other_payoff'])

    def set_c_payoffs(self):
        self.c_payoff = c(Constants.payoffs[1][self.c_option-1]['self_payoff'])
        self.c_other_payoff = c(Constants.payoffs[1][self.c_option-1]['other_payoff'])

    def finalize(self):
        if self.chosen_task == 1:
            self.payoff = c(self.a_payoff)
        elif self.chosen_task == 2:
            self.payoff = c(self.b_payoff)
        elif self.chosen_task == 3:
            self.payoff = c(self.c_payoff)

        self.participant.vars['t2_data'] = {
            'chosen_task': self.chosen_task,
            'payoff': self.payoff,
        }
