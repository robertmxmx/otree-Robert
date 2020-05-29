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
from functions import shift_groups

def points_taken():
    return models.BooleanField(
        label="Do you choose to take %d points from B or not?" % Constants.take_amount,
        choices=[
            [True, "Take %d points" % Constants.take_amount],
            [False, "Do not take %d points" % Constants.take_amount]
        ],
        widget=widgets.RadioSelect
    )
    
def points_retaliated():
    return models.CurrencyField(
        label="Amount you will spend on retaliation:",
        min=Constants.deduction['min'],
        max=Constants.deduction['max']
    )

class Constants(BaseConstants):
    name_in_url = 'task1'
    players_per_group = 2
    num_rounds = 1

    deduction = dict(min=0, max=5, multiplier=3)
    take_amount = 5
    initial_payoff = 10

    comprehension_answers = dict(
        c1=True, c2=initial_payoff, c3=2, c4=deduction['multiplier']
    )


class Subsession(BaseSubsession):
    def creating_session(self):
        group_matrix = shift_groups(self.get_group_matrix(), 1)
        self.set_group_matrix(group_matrix)
            

class Group(BaseGroup):
    points_taken = points_taken()
    points_retaliated = points_retaliated()

    def get_payoffs(self):
        return [
            dict(role=player.role(), payoff=player.payoff) 
            for player in self.get_players()
        ]

    def set_initial_payoffs(self):
        for player in self.get_players():
            player.payoff = c(Constants.initial_payoff)

    def set_final_payoffs(self):
        if self.points_taken:
            a_payoff = Constants.take_amount - (Constants.deduction['multiplier'] * self.points_retaliated)
            b_payoff = -Constants.take_amount - self.points_retaliated

            self.get_player_by_role('A').payoff += c(a_payoff)
            self.get_player_by_role('B').payoff += c(b_payoff)


class Player(BasePlayer):
    c1 = models.BooleanField(
        label='''If Participant A chooses to take, then Participant B will 
            have the opportunity to retaliate.''',
        choices=[[True, 'True'], [False, 'False']],
        widget=widgets.RadioSelect
    )
    c2 = models.CurrencyField(
        label='''If Participant A chooses not to take, how much will each 
            Participant earn from this task?'''
    )
    c3 = models.IntegerField(
        label='''If Participant A chooses to take, will Participant B earn 
            more or less by retaliating?''',
        choices=[
            [1, "Participant B will earn more by retaliating"],
            [2, "Participant B will earn less by retaliating"]
        ],
        widget=widgets.RadioSelect
    )
    c4 = models.CurrencyField(
        label='''If Participant B spends one point on retaliating, how 
            many points will A lose?'''
    )

    c1wrong = models.IntegerField(initial=0)
    c2wrong = models.IntegerField(initial=0)
    c3wrong = models.IntegerField(initial=0)
    c4wrong = models.IntegerField(initial=0)

    def role(self):
        if self.id_in_group == 1:
            return 'A'
        else:
            return 'B'