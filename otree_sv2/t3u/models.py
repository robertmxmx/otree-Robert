from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


class Constants(BaseConstants):
    name_in_url = 't3u'
    players_per_group = 2
    num_rounds = 1

    instructions_content = 't1u/InstructionsContent.html'
    total_points = 12
    dollar_per_point = 2
    labels = ["Much more likely", "", "", "Equally Likely", "", "", "Much less likely"]


class Subsession(BaseSubsession):

    def creating_session(self):
        # this will put players with even id as participant A and odd id as B
        r1_arr = [p for p in self.get_players() if p.participant.id_in_session % 2]
        r2_arr = [p for p in self.get_players() if not p.participant.id_in_session % 2]
        r2_arr.append(r2_arr.pop(0))
        if len(r1_arr) == len(r2_arr):
            self.set_group_matrix([list(a) for a in zip(r1_arr, r2_arr)])


def make_b_decision():
        return models.IntegerField(choices=[[1, "Accept"], [0, "Reject"]], widget=widgets.RadioSelectHorizontal)


class Group(BaseGroup):
    # Decision variables
    a_decision = models.IntegerField(choices=[
        [1, "11, 1"], [2, "10, 2"], [3, "9, 3"], [4, "8, 4"], [5, "7, 5"], [6, "6, 6"], [7, "5, 7"], [8, "4, 8"],
        [9, "3, 9"], [10, "2, 10"], [11, "1, 11"]
    ], initial=6, widget=widgets.RadioSelect)
    b_decision1 = make_b_decision()
    b_decision2 = make_b_decision()
    b_decision3 = make_b_decision()
    b_decision4 = make_b_decision()
    b_decision5 = make_b_decision()
    b_decision6 = make_b_decision()
    b_decision7 = make_b_decision()
    b_decision8 = make_b_decision()
    b_decision9 = make_b_decision()
    b_decision10 = make_b_decision()
    b_decision11 = make_b_decision()

    def set_payoffs(self):
        temp_arr = [self.b_decision1, self.b_decision2, self.b_decision3, self.b_decision4, self.b_decision5,
                    self.b_decision6, self.b_decision7, self.b_decision8, self.b_decision9, self.b_decision10,
                    self.b_decision11]

        p1_payoff = c(Constants.dollar_per_point * (Constants.total_points - self.a_decision)) if temp_arr[self.a_decision-1] else c(0)
        self.get_player_by_id(1).task_payoff = p1_payoff
        self.get_player_by_id(1).participant.vars['task_payoffs'].append(p1_payoff)

        p2_payoff = c(Constants.dollar_per_point * self.a_decision) if temp_arr[self.a_decision-1] else c(0)
        self.get_player_by_id(2).task_payoff = p2_payoff
        self.get_player_by_id(2).participant.vars['task_payoffs'].append(p2_payoff)


class Player(BasePlayer):
    # Survey variables
    survey_qa1 = models.IntegerField(
        choices=[[1, ""], [2, ""], [3, ""], [4, ""], [5, ""], [6, ""], [7, ""]],
        widget=widgets.RadioSelectHorizontal
    )
    survey_qb1 = models.IntegerField(
        choices=[[1, ""], [2, ""], [3, ""], [4, ""], [5, ""], [6, ""], [7, ""]],
        widget=widgets.RadioSelectHorizontal
    )
    task_payoff = models.CurrencyField()

