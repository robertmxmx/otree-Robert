from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


class Constants(BaseConstants):
    name_in_url = 'task5a'
    players_per_group = 2
    num_rounds = 6

    instructions_content = 'task2/InstructionsContent.html'

    initial_payoff = 0
    initial_points = 2
    multiplier = 3
    labels = ["Much more likely", "", "", "Equally Likely", "", "", "Much less likely"]


class Subsession(BaseSubsession):

    def creating_session(self):
        if self.round_number == 1:
            r1_arr = [p for p in self.get_players() if p.participant.id_in_session % 2 == 1]
            r2_arr = [p for p in self.get_players() if p.participant.id_in_session % 2 == 0]
            r2_arr.append(r2_arr.pop(0))
            r2_arr.append(r2_arr.pop(0))
            r2_arr.append(r2_arr.pop(0))
            if len(r1_arr) != len(r2_arr):
                print("not even amount of players")
            else:
                self.set_group_matrix([list(a) for a in zip(r1_arr, r2_arr)])
        else:
            self.group_like_round(1)


class Group(BaseGroup):
    # Participant Actions
    p1_sent = models.CurrencyField(initial=0)
    p2_sent = models.CurrencyField(initial=0)

    def set_payoffs(self):
        p1 = self.get_player_by_id(1)
        p2 = self.get_player_by_id(2)

        p1.payoff = Constants.initial_points - self.p1_sent + self.p2_sent
        p2.payoff = (Constants.multiplier * self.p1_sent) - self.p2_sent


class Player(BasePlayer):
    survey_q1 = models.IntegerField(
        choices=[[1, ""], [2, ""], [3, ""], [4, ""], [5, ""], [6, ""], [7, ""]],
        widget=widgets.RadioSelectHorizontal
    )
    survey_q2 = models.LongStringField()