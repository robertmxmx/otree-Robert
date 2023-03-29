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


def is_most_common(value, compare_list):
    """Check if <value> is the most commonly appearing value in <compare_list>"""

    try:
        list_mode = mode(compare_list)
    except StatisticsError:
        return None

    return value == list_mode


def get_B(group):
    return group.get_player_by_role("B")


def get_C(group):
    return group.get_player_by_role("C")


def make_deduct_field():
    return models.CurrencyField(
        min=Constants.deduct["min"], max=Constants.deduct["max"]
    )


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
        if len(waiting_players) > 0:
            group_num = waiting_players[0].participant.vars["group"]

            potential_group = []
            for p in waiting_players:
                if p.participant.vars["group"] == group_num:
                    potential_group.append(p)

            if len(potential_group) == Constants.players_per_group:
                return potential_group

    def creating_session(self):
        # Set player role for the round
        self.taking_player = "A"
        self.deducting_player = "B" if self.round_number == 1 else "C"

        if self.round_number != 1:
            self.group_like_round(1)


class Group(BaseGroup):
    def init_round(self):
        for p in self.get_players():
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

    def set_A_bonus_payoffs(self):
        guesses = {}
        player_A = self.get_player_by_role("A")
        other_groups = self.get_other_groups()
        similar_groups = self.get_similar_groups()

        if len(similar_groups) > 0:
            guesses["ee_a_group"] = is_most_common(
                player_A.ee_a_group, [get_B(g).deduct_amount for g in similar_groups]
            )

        guesses["ee_a_session"] = is_most_common(
            player_A.ee_a_session, [get_B(g).deduct_amount for g in other_groups]
        )

        if len(similar_groups) > 0:
            guesses["ne_a_b_group"] = is_most_common(
                player_A.ne_a_b_group, [get_B(g).ne_b for g in similar_groups]
            )

        guesses["ne_a_b_session"] = is_most_common(
            player_A.ne_a_b_session, [get_B(g).ne_b for g in other_groups]
        )

        if self.session.config["rep_condition"] and (len(similar_groups) > 0):
            guesses["ne_a_c_group"] = is_most_common(
                player_A.ne_a_c_group, [get_C(g).ne_c for g in similar_groups]
            )

        guesses["ne_a_c_session"] = is_most_common(
            player_A.ne_a_c_session, [get_C(g).ne_c for g in other_groups]
        )

        player_A.set_bonus(guesses)

    def set_B_bonus_payoffs(self):
        guesses = {}
        player_B = self.get_player_by_role("B")
        similar_groups = self.get_similar_groups()
        other_groups = self.get_other_groups()

        if len(similar_groups) > 0:
            guesses["ee_b_group"] = is_most_common(
                player_B.ee_b_group, [get_B(g).deduct_amount for g in similar_groups]
            )

        guesses["ee_b_session"] = is_most_common(
            player_B.ee_b_session, [get_B(g).deduct_amount for g in other_groups]
        )

        if len(similar_groups) > 0:
            guesses["ne_b_b_group"] = is_most_common(
                player_B.ne_b_b_group, [get_B(g).ne_b for g in similar_groups]
            )

        guesses["ne_b_b_session"] = is_most_common(
            player_B.ne_b_b_session, [get_B(g).ne_b for g in other_groups]
        )

        if self.session.config["rep_condition"] and (len(similar_groups) > 0):
            guesses["ne_b_c_group"] = is_most_common(
                player_B.ne_b_c_group, [get_C(g).ne_c for g in similar_groups]
            )

        guesses["ne_b_c_session"] = is_most_common(
            player_B.ne_b_c_session, [get_C(g).ne_c for g in other_groups]
        )

        player_B.set_bonus(guesses)

    def set_C_bonus_payoffs(self):
        guesses = {}  # Questions that the player correctly guessed
        player_C = self.get_player_by_role("C")
        similar_groups = self.get_similar_groups()
        other_groups = self.get_other_groups()

        if self.session.config["rep_condition"] and (len(similar_groups) > 0):
            guesses["ee_c_group"] = is_most_common(
                player_C.ee_c_group, [get_B(g).deduct_amount for g in similar_groups]
            )

        guesses["ee_c_session"] = is_most_common(
            player_C.ee_c_session, [get_B(g).deduct_amount for g in other_groups]
        )

        guesses["ne_c_c_session"] = is_most_common(
            player_C.ne_c_c_session, [get_C(g).ne_c for g in other_groups]
        )

        if self.session.config["rep_condition"] and (len(similar_groups) > 0):
            guesses["ne_c_c_group"] = is_most_common(
                player_C.ne_c_c_group, [get_C(g).ne_c for g in similar_groups]
            )

        player_C.set_bonus(guesses)

    def set_payoffs(self):
        deduct_role = self.subsession.deducting_player
        deduct_amount = self.get_player_by_role(deduct_role).deduct_amount
        playerA = self.get_player_by_role("A")

        payoffs = { **Constants.initial_payoffs }

        # Set if ECU was taken
        if playerA.chose_to_take:
            payoffs["A"] = payoffs["A"] + Constants.take_amount
            payoffs[deduct_role] = payoffs[deduct_role] - Constants.take_amount

        # Set all players payoff after the choice of whether to take
        for player in self.get_players():
            player.payoff_after_take = payoffs[player.role()]

        # Set deduction amount
        if playerA.chose_to_take:
            payoffs["A"] = payoffs["A"] - (
                Constants.deduct["multiplier"] * int(deduct_amount)
            )
            payoffs[deduct_role] = payoffs[deduct_role] - int(deduct_amount)

        # Set payoff for game. final_payoff is not really the final payoff,
        # but the final payoff BEFORE bonuses are given
        for player in self.get_players():
            player.final_payoff = payoffs[player.role()]

        # Set payoffs for Bonus Questions
        if self.round_number == 1:
            self.set_A_bonus_payoffs()
            self.set_B_bonus_payoffs()
            self.set_C_bonus_payoffs()


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
    comp3 = models.IntegerField(
        label=(
            "In Task 2, before making a decision, will A learn how B reacted "
            "to A's decision in Task 1?"
        ),
        widget=widgets.RadioSelect,
        choices=[
            [1, "Yes, A will learn, regardless of whether A takes from B in Task 1"],
            [2, "Yes, A will learn, provided A takes from B in Task 1"],
            [3, "No, A will not learn how B reacted in Task 1"],
        ],
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

    # Even though this is named final_payoff, this does not include the bonus
    # for the belief questions
    final_payoff = models.CurrencyField()

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

    bonus_q_to_pay = models.StringField()
    bonus_paid = models.BooleanField(initial=False)

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

    def set_bonus(self, guesses):
        chosen_question = random.choice(list(guesses.keys()))

        self.bonus_q_to_pay = chosen_question
        self.participant.vars["belief_bonus"] = {
            "paid": False,
            "question": chosen_question,
            "amount": None,
        }

        if guesses[chosen_question]:
            bonus = Constants.additional_amount

            self.bonus_paid = True

            self.participant.vars["belief_bonus"]["paid"] = True
            self.participant.vars["belief_bonus"]["amount"] = bonus
