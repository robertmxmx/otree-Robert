from otree.api import Currency as c
from . import pages
from ._builtin import Bot
from .models import Constants
from otree.api import Submission

from _myshared.constants import SortTypes

CHOSE_TO_TAKE = True
DEDUCT_AMOUNT = 5

BONUS_ANSWERS = {
    "A": {
        "base": {
            "ee_a_session": 5,
            "ne_a": 5,
            "ne_a_b_session": 5,
            "ne_a_c_session": 5,
        },
        "same_grouping": {
            "ee_a_group": 5,
            "ne_a_b_group": 5,
        },
        "rep_condition": {
            "ne_a_c_group": 5,
        },
    },
    "B": {
        "base": {
            "ee_b_session": 5,
            "ne_b": 5,
            "ne_b_b_session": 5,
            "ne_b_c_session": 5,
        },
        "same_grouping": {
            "ee_b_group": 5,
            "ne_b_b_group": 5,
        },
        "rep_condition": {
            "ne_b_c_group": 5,
        },
    },
    "C": {
        "base": {
            "ee_c_session": 5,
            "ne_c": 5,
            "ne_c_c_session": 5,
        },
        "same_grouping": {},
        "rep_condition": {
            "ee_c_group": 5,
            "ne_c_c_group": 5,
        },
    },
}


def get_bouns_answers(role, rep_condition, same_grouping):
    role_answers = BONUS_ANSWERS[role]
    answers = {**role_answers["base"]}

    if same_grouping:
        answers = {**answers, **role_answers["same_grouping"]}

        if rep_condition:
            answers = {**answers, **role_answers["rep_condition"]}

    return answers

"""
Return a list of sort types where these sort types have more than 1 group.
For example: if there are 2 birth region groups and 1 political ideology group
this array will return: ["birth_region"]
"""
def get_same_groupings(players):
    birth_region_players = 0
    political_ideology_players = 0
    same_groupings = []
    
    for player in players:
        sorted_by = player.participant.vars["sorted_by"]

        if sorted_by == SortTypes.NONE.value:
            continue
        elif sorted_by == SortTypes.BIRTH_REGION.value:
            birth_region_players += 1
        elif sorted_by == SortTypes.POLITICAL_IDEOLOGY.value:
            political_ideology_players += 1

    if birth_region_players > Constants.players_per_group:
        same_groupings.append(SortTypes.BIRTH_REGION.value)

    if political_ideology_players > Constants.players_per_group:
        same_groupings.append(SortTypes.POLITICAL_IDEOLOGY.value)

    return same_groupings


class PlayerBot(Bot):
    def play_round(self):
        if "group" not in self.participant.vars:
            return

        rep_condition = self.session.config["rep_condition"]
        round_num = self.round_number

        if round_num == 1:
            yield Submission(pages.Instructions, check_html=False)
            yield Submission(pages.Instructions2)
            yield Submission(pages.VideoInstructions, check_html=False)
            yield Submission(pages.Instructions3, check_html=False)
            yield Submission(pages.Instructions3a, check_html=False)
            yield Submission(pages.Instructions4, check_html=False)

            comp_answers = {
                "comp1": 1,
                "comp2": True,
                "comp3": 1 if self.session.config["deterrence"] else 3,
                "comp5": 36,
            }

            if rep_condition:
                comp_answers["comp4"] = 2

            yield (pages.Comprehension, comp_answers)

        yield pages.Commencement

        if self.player.role() == self.subsession.taking_player:
            yield (pages.TakingDecision, {"chose_to_take": CHOSE_TO_TAKE})
        elif self.player.role() == self.subsession.deducting_player:
            yield Submission(
                pages.DeductingDecision,
                {"deduct_amount": DEDUCT_AMOUNT},
                check_html=False,
            )

        if round_num == 1:
            same_groupings = get_same_groupings(self.subsession.get_players())
            same_grouping = self.participant.vars["sorted_by"] in same_groupings

            answers = get_bouns_answers(
                self.player.role(), rep_condition, same_grouping
            )

            yield (pages.BonusQuestions, answers)

        expected_payoff = Constants.initial_payoffs[self.player.role()]

        # Calculate normal payoffs
        if self.player.role() == "A" and CHOSE_TO_TAKE:
            expected_payoff += Constants.take_amount - (
                Constants.deduct["multiplier"] * DEDUCT_AMOUNT
            )
        elif CHOSE_TO_TAKE and (
            (round_num == 1 and self.player.role() == "B")
            or (round_num == 2 and self.player.role() == "C")
        ):
            expected_payoff -= Constants.take_amount + DEDUCT_AMOUNT

        # TODO: Needs to be more specific.
        # e.g. ee_c_session == playerB.deduct_amount
        q_to_pay = self.player.field_maybe_none("bonus_q_to_pay")
        if self.player.field_maybe_none(q_to_pay) == 5:
            assert self.player.bonus_paid == True

        error_message = (
            f"Player {self.player.role()} - "
            f"Actual Payoff: {self.player.final_payoff}, "
            f"Expected Payoff: {c(expected_payoff)}"
        )
        assert self.player.final_payoff == c(expected_payoff), error_message

        yield pages.Feedback

        if rep_condition and round_num == 2:
            yield pages.CMessage
