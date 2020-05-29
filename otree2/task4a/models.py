from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


class Constants(BaseConstants):
    name_in_url = 'task4a'
    players_per_group = 2
    num_rounds = 6

    instructions_content = 'task1/InstructionsContent.html'
    initial_payoff = 12
    labels = ["Much more likely", "", "", "Equally Likely", "", "", "Much less likely"]


class Subsession(BaseSubsession):

    def creating_session(self):
        if self.round_number == 1:
            r1_arr = [p for p in self.get_players() if p.participant.id_in_session % 2 == 1]
            r2_arr = [p for p in self.get_players() if p.participant.id_in_session % 2 == 0]
            r2_arr.append(r2_arr.pop(0))
            r2_arr.append(r2_arr.pop(0))
            if len(r1_arr) != len(r2_arr):
                print("not even amount of players")
            else:
                self.set_group_matrix([list(a) for a in zip(r1_arr, r2_arr)])
        else:
            self.group_like_round(1)


class Group(BaseGroup):
    r1_action = models.StringField(choices=[
            "CHALLENGE",
            "DO NOTHING"
        ], widget=widgets.RadioSelect)
    r2_action = models.StringField(label="Do you wish to:",  choices=[
            "RETALIATE",
            "DEFER"
        ], widget=widgets.RadioSelect)

    def set_payoffs(self):
        r1_player = self.get_player_by_id(1)
        r2_player = self.get_player_by_id(2)

        if self.r1_action == "CHALLENGE":
            if self.r2_action == "RETALIATE":
                r1_player.payoff = c(-2)
                r2_player.payoff = c(-2)
            elif self.r2_action == "DEFER":
                r1_player.payoff = c(2)
            else:
                print("ERROR: Invalid action for Role 2 player")
        elif self.r1_action == "DO NOTHING":
            r1_player.payoff = c(1)
            r2_player.payoff = c(1)
        else:
            print("ERROR: Invalid action for Role 1 player")


class Player(BasePlayer):
    survey_q1 = models.IntegerField(
        choices=[[1, ""], [2, ""], [3, ""], [4, ""], [5, ""], [6, ""], [7, ""]],
        widget=widgets.RadioSelectHorizontal
    )
    survey_q2 = models.LongStringField()