from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
)
from statistics import mode, StatisticsError

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

            # Check if grouped by birth region and has same
            # birth regions as current group
            current_brs = [p.br for p in current_players]
            other_brs = [p.br for p in players]
            same_birth_region = (current_sort == SortTypes.BIRTH_REGION.value) and (
                sorted(current_brs) == sorted(other_brs)
            )

            # Check if grouped by politicial ideology ans has same ideology as
            # current group
            current_pis = [p.pi for p in current_players]
            other_pis = [p.pi for p in players]
            same_political_ideology = (
                current_sort == SortTypes.POLITICAL_IDEOLOGY.value
            ) and (sorted(current_pis) == sorted(other_pis))

            if same_birth_region or same_political_ideology:
                similar_groups.append(group)

        return similar_groups

    def set_round1_other_payoffs(self, similar_groups):
        """Sets the payoff for the "other" player in round 1"""
        playerC = self.get_player_by_role("C")
        bonus = 0

        if playerC.will_spend == self.get_player_by_role("B").deduct_amount:
            bonus += Constants.additional_amount

        if len(similar_groups) > 0:
            answers = [g.get_player_by_role("C").should_spend for g in similar_groups]

            try:
                most_common_answer = mode(answers)
            except StatisticsError:
                most_common_answer = None

            if most_common_answer and (
                playerC.same_grouping_should_spend == most_common_answer
            ):
                bonus += Constants.additional_amount

        playerC.payoff += bonus
        playerC.participant.vars["bonuses"]["task1"] = bonus

    def set_round2_other_payoffs(self, similar_groups):
        """Sets the payoff for the "other" player in round 1"""
        bonus = 0
        playerB = self.get_player_by_role("B")

        other_groups = [g for g in self.subsession.get_groups() if g.id != self.id]
        deductions = []

        for group in other_groups:
            # Player B in round 2 was the deducting player in round 1
            deductions.append(group.get_player_by_role("B").in_round(1).deduct_amount)

        try:
            most_common_deduction = mode(deductions)
        except StatisticsError:
            most_common_deduction = None

        if most_common_deduction and (
            playerB.general_deduction == most_common_deduction
        ):
            bonus += Constants.additional_amount

        if len(similar_groups) > 0:
            similar_groups = self.get_similar_groups()

            deductions = []
            for group in similar_groups:
                # Player B in round 2 was the deducting player in round 1
                deductions.append(
                    group.get_player_by_role("B").in_round(1).deduct_amount
                )

            try:
                most_common_deduction = mode(deductions)
            except StatisticsError:
                most_common_deduction = None

            if most_common_deduction and (
                playerB.same_grouping_deduction == most_common_deduction
            ):
                bonus += Constants.additional_amount

            should_spend_answers = []
            for group in similar_groups:
                should_spend_answers.append(
                    group.get_player_by_role("C").in_round(1).should_spend
                )

            try:
                most_common_answer = mode(should_spend_answers)
            except StatisticsError:
                most_common_answer = None

            if most_common_answer and (
                playerB.should_spend_guess == most_common_answer
            ):
                bonus += Constants.additional_amount

        playerB.payoff += bonus
        playerB.participant.vars["bonuses"]["task2"] = bonus

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

        similar_groups = self.get_similar_groups()

        # Set payoffs for B/C guess
        if self.round_number == 1:
            self.set_round1_other_payoffs(similar_groups)
        else:
            self.set_round2_other_payoffs(similar_groups)


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

    will_spend = models.CurrencyField(
        min=Constants.deduct["min"], max=Constants.deduct["max"]
    )
    should_spend = models.CurrencyField(
        min=Constants.deduct["min"], max=Constants.deduct["max"]
    )
    same_grouping_should_spend = models.CurrencyField(
        min=Constants.deduct["min"], max=Constants.deduct["max"]
    )

    general_deduction = models.CurrencyField(
        min=Constants.deduct["min"], max=Constants.deduct["max"]
    )
    same_grouping_deduction = models.CurrencyField(
        min=Constants.deduct["min"], max=Constants.deduct["max"]
    )
    should_spend_guess = models.CurrencyField(
        min=Constants.deduct["min"], max=Constants.deduct["max"]
    )

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
