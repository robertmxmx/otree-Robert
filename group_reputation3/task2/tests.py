from otree.api import Currency as c
from . import pages
from ._builtin import Bot
from .models import Constants
from otree.api import Submission

# Test cases. Uncomment the specific case to use. NOTE: Remember to use the same
# case in Task 1 tests
CASE = "no_grouping"
# CASE = "group_by_birth"
# CASE = "group_by_politics"

CHOSE_TO_TAKE = True
DEDUCT_AMOUNT = 5
WILL_SPEND = 5
SAME_GROUPING_SHOULD_SPEND = 5
SHOULD_SPEND = 5
GENERAL_DEDUCTION = 5
SAME_GROUPING_DEDUCTION = 5
SHOULD_SPEND_GUESS = 5


class PlayerBot(Bot):
    def play_round(self):
        if "group" not in self.participant.vars:
            return

        if self.round_number == 1:
            yield Submission(pages.Instructions, check_html=False)
            yield Submission(pages.Instructions2)
            yield Submission(pages.VideoInstructions, check_html=False)
            yield Submission(pages.Instructions3, check_html=False)
            yield Submission(pages.Instructions3a, check_html=False)
            yield Submission(pages.Instructions4, check_html=False)

            comp_answers = {
                "comp1": 1,
                "comp2": True,
                "comp3": self.session.config["deterrence"],
                "comp5": 36,
            }

            if self.session.config["rep_condition"]:
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
        else:
            if self.round_number == 1:
                answers = {"will_spend": WILL_SPEND, "should_spend": SHOULD_SPEND}

                if CASE != "no_grouping":
                    answers = {
                        **answers,
                        "same_grouping_should_spend": SAME_GROUPING_SHOULD_SPEND,
                    }
            else:
                answers = {"general_deduction": GENERAL_DEDUCTION}

                if CASE != "no_grouping":
                    answers = {
                        **answers,
                        "same_grouping_deduction": SAME_GROUPING_DEDUCTION,
                        "should_spend_guess": SHOULD_SPEND_GUESS,
                    }

            yield (pages.WaitingDecision, answers)

        expected_payoff = Constants.initial_payoffs[self.player.role()]

        if self.round_number == 1:
            if (self.player.role() == "A") and CHOSE_TO_TAKE:
                expected_payoff += Constants.take_amount - (
                    Constants.deduct["multiplier"] * DEDUCT_AMOUNT
                )
            elif (self.player.role() == "B") and CHOSE_TO_TAKE:
                expected_payoff -= Constants.take_amount + DEDUCT_AMOUNT
            elif self.player.role() == "C":
                if WILL_SPEND == DEDUCT_AMOUNT:
                    expected_payoff += Constants.additional_amount

                if (CASE != "no_grouping") and (
                    SHOULD_SPEND == SAME_GROUPING_SHOULD_SPEND
                ):
                    expected_payoff += Constants.additional_amount
        else:
            if (self.player.role() == "A") and CHOSE_TO_TAKE:
                expected_payoff += Constants.take_amount - (
                    Constants.deduct["multiplier"] * DEDUCT_AMOUNT
                )
            elif self.player.role() == "B":
                if DEDUCT_AMOUNT == GENERAL_DEDUCTION:
                    expected_payoff += Constants.additional_amount

                if CASE != "no_grouping":
                    if DEDUCT_AMOUNT == SAME_GROUPING_DEDUCTION:
                        expected_payoff += Constants.additional_amount

                    if SHOULD_SPEND == SHOULD_SPEND_GUESS:
                        expected_payoff += Constants.additional_amount
            elif (self.player.role() == "C") and CHOSE_TO_TAKE:
                expected_payoff -= Constants.take_amount + DEDUCT_AMOUNT

        error_message = (
            f"Player: {self.player.role()}, "
            f"Actual Payoff: {self.player.payoff}, "
            f"Expected Payoff: {c(expected_payoff)}"
        )
        assert self.player.payoff == c(expected_payoff), error_message

        yield pages.Feedback

        if self.session.config["rep_condition"] and self.round_number == 2:
            yield pages.CMessage
