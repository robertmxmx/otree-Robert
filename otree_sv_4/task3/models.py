from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)
import constants
from functions import shift_groups

import task1.models as t1_models


class Constants(BaseConstants):
    name_in_url = 'task3'
    players_per_group = 2
    num_rounds = 1

    statements = constants.statements
    reveal_statements = constants.reveal_statements

    deduction = t1_models.Constants.deduction
    take_amount = t1_models.Constants.take_amount
    initial_payoff = t1_models.Constants.initial_payoff
    
    opt_out_text = constants.opt_out_text

    likert_likely = [
        [1, 'Much more likely'], [2, ''], [3, ''], [4, 'Equally likely'], 
        [5, ''], [6, ''], [7, 'Much less likely']
    ]


class Subsession(BaseSubsession):
    def creating_session(self):
        group_matrix = shift_groups(self.get_group_matrix(), 2)
        self.set_group_matrix(group_matrix)

    def reset_payoff(self):
        for player in self.get_players():
            player.participant.payoff = 0


class Group(BaseGroup):
    points_taken = t1_models.points_taken()
    points_retaliated = t1_models.points_retaliated()

    def get_payoffs(self):
        return t1_models.Group.get_payoffs(self)

    def set_initial_payoffs(self):
        t1_models.Group.set_initial_payoffs(self)

    def set_final_payoffs(self):
        t1_models.Group.set_final_payoffs(self)


class Player(BasePlayer):
    surveyq_part_A = models.IntegerField(
        label='''Did you think that your partner in this task was more or less 
            likely to retaliate than your partner in task 1?''',
        choices=Constants.likert_likely,
        widget=widgets.RadioSelect
    )
    surveyq_part_B = models.IntegerField(
        label='''Did you think that your partner in this task was more or 
            less likely to take points from you than your partner in task 1?''',
        choices=Constants.likert_likely, 
        widget=widgets.RadioSelect
    )
    surveyq_why = models.LongStringField(label='Why?')

    def role(self):
        return t1_models.Player.role(self)
