from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
)
from statistics import mode, StatisticsError
import random

from _myshared.constants import REGIONS, SortTypes


class Constants(BaseConstants):
    name_in_url = "task2"
    players_per_group = 3
    num_rounds = 2

    initial_payoffs = {"A": 20, "B": 110, "C": 110}
    take_amount = 100
    deduct = {"min": 0, "max": 10, "multiplier": 12}
    additional_amount = 10


class Subsession(BaseSubsession):
    taking_player = models.StringField()
    deducting_player = models.StringField()

    def group_by_arrival_time_method(self, waiting_players):
        group_num = waiting_players[0].participant.vars["group"]

        potential_group = []
        for p in waiting_players:
            if p.participant.vars["group"] == group_num:
                potential_group.append(p)

        if len(potential_group) == Constants.players_per_group:
            return potential_group

    def creating_session(self):
        for p in self.get_players():
            p.participant.vars["bonuses"] = {"task1": 0, "task2": 0}

        # Set player role for the round
        self.taking_player = "A"
        self.deducting_player = "B" if self.round_number == 1 else "C"

        if self.round_number != 1:
            self.group_like_round(1)


def is_most_common(value, compare_list):
    """
    Check if <value> is the most commonly appearing value in <compare_list>
    """

    try:
        list_mode = mode(compare_list)
    except StatisticsError:
        return None

    return value == list_mode


class Group(BaseGroup):
    def init_round(self):
        for p in self.get_players():
            p.participant.payoff = 0
            p.payoff = Constants.initial_payoffs[p.role()]
            p.br = p.participant.vars["birth_region"]
            p.pi = p.participant.vars["pol_ideology"]

    def get_similar_groups(self):
        """
        Returns a list of groups (other that the current one) that have been
        sorted the same as the current group
        """
        current_players = self.get_players()
        current_sort = current_players[0].participant.vars["sorted_by"]

        if not current_sort:
            return []

        similar_groups = []

        for group in self.subsession.get_groups():
            players = group.get_players()
            same_sort_type = any(
                p.participant.vars["sorted_by"] == current_sort for p in players
            )

            if (group.id == self.id) or not same_sort_type:
                continue

            if current_sort == SortTypes.BIRTH_REGION.value:
                # Check if grouped by birth region and has same
                # birth regions as current group

                current_brs = [p.br for p in current_players]
                other_brs = [p.br for p in players]

                if sorted(current_brs) == sorted(other_brs):
                    similar_groups.append(group)
            elif current_sort == SortTypes.POLITICAL_IDEOLOGY.value:
                # Check if grouped by politicial ideology and has same
                # ideology as current group

                current_pis = [p.pi for p in current_players]
                other_pis = [p.pi for p in players]

                if sorted(current_pis) == sorted(other_pis):
                    similar_groups.append(group)

        return similar_groups

    def get_other_groups(self):
        return [g for g in self.subsession.get_groups() if g != self.id]

    def set_round1_belief_questions_payoffs(self):
        """Sets the payoff for player C in round 1"""

        guesses = {} # Questions that the player correctly guessed
        player_C = self.get_player_by_role("C")
        similar_groups = self.get_similar_groups()
        other_groups = self.get_other_groups()

        if self.session.config["rep_condition"] and (len(similar_groups) > 0):
            guesses["1"] = is_most_common(
                player_C.ee_c_group,
                [g.get_player_by_role("B").deduct_amount for g in similar_groups]
            )

        guesses["2"] = is_most_common(
            player_C.ee_c_session,
            [g.get_player_by_role("B").deduct_amount for g in other_groups]
        )

        guesses["5"] = is_most_common(
            player_C.ne_c_c_session,
            [g.get_player_by_role("C").ne_c for g in other_groups]
        )


        if self.session.config["rep_condition"] and (len(similar_groups) > 0):
            guesses["4"] = is_most_common(
                player_C.ne_c_c_group,
                [g.get_player_by_role("C").ne_c for g in similar_groups]
            )

        player_C.set_bonus_payoff(guesses, "task1")

    def set_round2_belief_questions_payoff(self):
        """Sets the payoff for player B in round 2"""

        def get_round1_C(group):
            """Get the round 1 data for Player C"""
            return group.get_player_by_role("C").in_round(1)

        def get_round1_B(group):
            """Get the round 1 data for Player B"""
            return group.get_player_by_role("B").in_round(1)

        guesses = {}
        player_B = self.get_player_by_role("B")
        similar_groups = self.get_similar_groups()
        other_groups = self.get_other_groups()

        if len(similar_groups) > 0:
            guesses["1"] = is_most_common(
                player_B.ee_b_group,
                [get_round1_B(g).deduct_amount for g in similar_groups]
            )

        guesses["2"] = is_most_common(
            player_B.ee_b_session,
            [get_round1_B(g).deduct_amount for g in other_groups]
        )

        if len(similar_groups) > 0:
            guesses["4"] = is_most_common(
                player_B.ne_b_b_group,
                [g.get_player_by_role("B").ne_b for g in similar_groups]
            )

        guesses["5"] = is_most_common(
            player_B.ne_b_b_session,
            [g.get_player_by_role("B").ne_b for g in other_groups]
        )

        if self.session.config["rep_condition"] and (len(similar_groups) > 0):
            guesses["6"] = is_most_common(
                player_B.ne_b_c_group,
                [get_round1_C(g).ne_c for g in similar_groups]
            )

        guesses["7"] = is_most_common(
            player_B.ne_b_c_session,
            [get_round1_C(g).ne_c for g in other_groups]
        )

        player_B.set_bonus_payoff(guesses, "task2")

    def set_payoffs(self):
        playerA = self.get_player_by_role("A")
        deducting_player = self.get_player_by_role(self.subsession.deducting_player)

        # Set if ECU was taken
        if playerA.chose_to_take:
            deducting_player.payoff -= Constants.take_amount
            playerA.payoff += Constants.take_amount

        # Set all players payoff after the choice of whether to take
        for p in self.get_players():
            p.payoff_after_take = p.participant.payoff

        # Set deduction amount
        if playerA.chose_to_take:
            deducting_player.payoff -= deducting_player.deduct_amount
            playerA.payoff -= (
                Constants.deduct["multiplier"] * deducting_player.deduct_amount
            )

        # Set payoffs for B/C guess
        if self.round_number == 1:
            self.set_round1_belief_questions_payoffs()
        else:
            self.set_round2_belief_questions_payoff()

    def set_end_belief_questions_payoffs(self):
        """
        Sets the payoff for Player C for Bonus Questions at end of experiment
        """

        def get_round1_B(group):
            """Get the round 1 data for Player B"""
            return group.get_player_by_role("B").in_round(1)

        def get_round1_C(group):
            """Get the round 1 data for Player C"""
            return group.get_player_by_role("C").in_round(1)

        guesses = {}
        player_A = self.get_player_by_role("A")
        other_groups = self.get_other_groups()
        similar_groups = self.get_similar_groups()

        if len(similar_groups) > 0:
            guesses["1"] = is_most_common(
                player_A.ee_a_group,
                [get_round1_B(g).deduct_amount for g in similar_groups]
            )

        guesses["2"] = is_most_common(
            player_A.ee_a_session,
            [get_round1_B(g).deduct_amount for g in other_groups]
        )
            
        if len(similar_groups) > 0:
            guesses["4"] = is_most_common(
                player_A.ne_a_b_group,
                [g.get_player_by_role("B").ne_b for g in similar_groups]
            )

        guesses["5"] = is_most_common(
            player_A.ne_a_b_session,
            [g.get_player_by_role("B").ne_b for g in other_groups]
        )

        if self.session.config["rep_condition"] and (len(similar_groups) > 0):
            guesses["6"] = is_most_common(
                player_A.ne_a_c_group,
                [get_round1_C(g).ne_c for g in similar_groups]
            )

        guesses["7"] = is_most_common(
            player_A.ne_a_c_session,
            [get_round1_C(g).ne_c for g in other_groups]
        )

        player_A.set_bonus_payoff(guesses, "end")


def make_deduct_field():
    return models.CurrencyField(
        min=Constants.deduct["min"], max=Constants.deduct["max"]
    )

class Player(BasePlayer):
    br = models.IntegerField()
    pi = models.IntegerField()

    comp1 = models.IntegerField(
        label="In Task 1, who will A have the opportunity to take ECU from?",
        choices=[[1, "B"], [2, "C"], [3, "both B and C"]],
        widget=widgets.RadioSelect,
    )
    comp2 = models.BooleanField(
        label="In Task 2, will A have the opportunity to take ECU from C?",
        widget=widgets.RadioSelectHorizontal,
        choices=[[True, "Yes"], [False, "No"]],
    )
    comp3 = models.BooleanField(
        label=(
            "In Task 2, before making a decision, will A learn how B reacted "
            "to A's decision in Task 1?"
        ),
        widget=widgets.RadioSelectHorizontal,
        choices=[[True, "Yes"], [False, "No"]],
    )
    comp4 = models.IntegerField(
        label="When will C learn about the membership of the group?",
        choices=[
            [1, "at the end of task 1"],
            [2, "at the end of task 2"],
            [3, "never"],
        ],
        widget=widgets.RadioSelect,
    )
    comp5 = models.IntegerField(
        label=(
            "If, after A takes ECU from B, Participant B chooses to spend 3 "
            "ECU to reduce A's endowment, how many ECU will A lose?"
        ),
        min=0,
    )
    comp1_wrong = models.IntegerField(initial=0)
    comp2_wrong = models.IntegerField(initial=0)
    comp3_wrong = models.IntegerField(initial=0)
    comp4_wrong = models.IntegerField(initial=0)
    comp5_wrong = models.IntegerField(initial=0)

    chose_to_take = models.BooleanField()
    payoff_after_take = models.CurrencyField()
    deduct_amount = models.CurrencyField(
        initial=0, min=Constants.deduct["min"], max=Constants.deduct["max"]
    )

    ee_c_group = make_deduct_field()
    ee_c_session = make_deduct_field()
    ne_c = make_deduct_field()
    ne_c_c_group = make_deduct_field()
    ne_c_c_session = make_deduct_field()

    ee_b_group = make_deduct_field()
    ee_b_session = make_deduct_field()
    ne_b = make_deduct_field()
    ne_b_b_group = make_deduct_field()
    ne_b_b_session = make_deduct_field()
    ne_b_c_group = make_deduct_field()
    ne_b_c_session = make_deduct_field()

    ee_a_group = make_deduct_field()
    ee_a_session = make_deduct_field()
    ne_a = make_deduct_field()
    ne_a_b_group = make_deduct_field()
    ne_a_b_session = make_deduct_field()
    ne_a_c_group = make_deduct_field()
    ne_a_c_session = make_deduct_field()

    def role(self):
        return self.participant.vars["role"]

    def get_instruction_vars(self):
        """Returns variables that are used on the instruction screen"""

        sorted_by = self.participant.vars["sorted_by"]
        deducting_player = self.group.get_player_by_role(
            self.subsession.deducting_player
        )

        return_dict = {"sorted_by": sorted_by}
        if sorted_by:
            return_dict["other_knowledge_player"] = (
                self.subsession.deducting_player
                if self.role() == self.subsession.taking_player
                else self.subsession.taking_player
            )

            if sorted_by == "birth_region":
                return_dict["same_region"] = REGIONS[deducting_player.br - 1]
            elif sorted_by == "pol_ideology":
                return_dict["same_ideology"] = (
                    "progressive" if deducting_player.pi == 1 else "conservative"
                )

        return return_dict

    def set_bonus_payoff(self, guesses, label):
        print("Setting bonus payoff for", label)
        print("Correct Guesses", guesses)

        # Needs to be stored in a variable?
        chosen_question = random.choice(list(guesses.keys()))
        print("Chosen Question: ", chosen_question)

        if guesses[chosen_question]:
            bonus = Constants.additional_amount
            self.payoff += bonus
            self.participant.vars["bonuses"][label] = bonus
