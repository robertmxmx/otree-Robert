from otree.api import Currency as c
from . import pages
from ._builtin import Bot
from .models import Constants
from otree.api import Submission

from _myshared.constants import SortTypes

CHOSE_TO_TAKE = True
DEDUCT_AMOUNT = 5

BONUS_ANSWERS = {
    "ee_a_session": 5,
    "ne_a": 5,
    "ne_a_b_session": 5,
    "ne_a_c_session": 5,
    "ee_a_group": 5,
    "ne_a_b_group": 5,
    "ne_a_c_group": 5,

    "ee_b_session": 5,
    "ne_b": 5,
    "ne_b_b_session": 5,
    "ne_b_c_session": 5,
    "ee_b_group": 5,
    "ne_b_b_group": 5,
    "ne_b_c_group": 5,

    "ee_c_session": 5,
    "ne_c": 5,
    "ne_c_c_session": 5,
    "ee_c_group": 5,
    "ne_c_c_group": 5,
}

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
            question_list = self.player.get_bonus_questions()
            answers = dict(
                (question, BONUS_ANSWERS[question]) for question in question_list
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
