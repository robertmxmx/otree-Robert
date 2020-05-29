from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


class Constants(BaseConstants):
    name_in_url = 't1t'
    players_per_group = 2
    num_rounds = 1

    instructions_content = 't1t/InstructionsContent.html'
    total_points = 12
    a_initial_points = 4
    dollar_per_point = 2


class Subsession(BaseSubsession):

    def creating_session(self):
        # this will put players with even id as participant A and odd id as B
        r1_arr = [p for p in self.get_players() if p.participant.id_in_session % 2]
        r2_arr = [p for p in self.get_players() if not p.participant.id_in_session % 2]
        if len(r1_arr) == len(r2_arr):
            self.set_group_matrix([list(a) for a in zip(r1_arr, r2_arr)])


class Group(BaseGroup):
    a_transfer = models.CurrencyField(choices=[i for i in range(0, Constants.a_initial_points + 1)])
    b_transfer1 = models.CurrencyField(choices=[0.5*i for i in range(0, 2*(1*3) + 1)])
    b_transfer2 = models.CurrencyField(choices=[0.5*i for i in range(0, 2*(2*3) + 1)])
    b_transfer3 = models.CurrencyField(choices=[0.5*i for i in range(0, 2*(3*3) + 1)])
    b_transfer4 = models.CurrencyField(choices=[0.5*i for i in range(0, 2*(4*3) + 1)])
    b_transfer = models.CurrencyField()     # the final amount that was transferred from B

    def set_payoffs(self):
        temp_arr = [0, self.b_transfer1, self.b_transfer2, self.b_transfer3, self.b_transfer4]
        self.b_transfer = c(temp_arr[int(self.a_transfer)])

        p1_payoff = c(Constants.dollar_per_point * (Constants.a_initial_points - self.a_transfer + self.b_transfer))
        self.get_player_by_id(1).task_payoff = p1_payoff
        self.get_player_by_id(1).participant.vars['task_payoffs'].append(p1_payoff)

        p2_payoff = c(Constants.dollar_per_point * (3*self.a_transfer - self.b_transfer))
        self.get_player_by_id(2).participant.vars['task_payoffs'].append(p2_payoff)
        self.get_player_by_id(2).task_payoff = p2_payoff


class Player(BasePlayer):
    # Comprehension Questions 1
    c1 = models.IntegerField(choices=[
        [1, '1 point'],
        [2, '2 points'],
        [3, '3 points'],
        [4, '0 points']
    ], widget=widgets.RadioSelect)
    c1_wrong = models.IntegerField(initial=0)
    # Comprehension Questions 2
    c2 = models.IntegerField(choices=[
        [1, 'No points can be sent back'],
        [2, '1 point at most can be sent back'],
        [3, 'Participant B can send back 0 points or 3 points only'],
        [4, 'Participant B can send back any amount of points from 0 to 3']
    ], widget=widgets.RadioSelect)
    c2_wrong = models.IntegerField(initial=0)
    task_payoff = models.CurrencyField()
