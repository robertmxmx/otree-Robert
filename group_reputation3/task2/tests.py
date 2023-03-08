from otree.api import Currency as c
from . import pages
from ._builtin import Bot
from .models import Constants
from otree.api import Submission

# Test cases. Uncomment the specific case to use. NOTE: Remember to use the same
# case in Task 1 tests
# CASE = "no_grouping"
# CASE = "group_by_birth"
CASE = "group_by_politics"

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
                answers = { "ee_c_session": 5, "ne_c": 5, "ne_c_c_session": 5 }

                if self.session.config["rep_condition"] and CASE != "no_grouping":
                    answers = { **answers, "ee_c_group": 5, "ne_c_c_group": 5 }
            else:
                answers = {
                    "ee_b_session": 5, 
                    "ne_b": 5, 
                    "ne_b_b_session": 5, 
                    "ne_b_c_session": 5,
                }

                if CASE != "no_grouping":
                    answers = { **answers, "ee_b_group": 5, "ne_b_c_group": 5 }

                    if self.session.config["rep_condition"]:
                        answers = { **answers, "ne_b_b_group": 5 }

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
                # TODO: Bonus question logic
                expected_payoff = None
        else:
            if (self.player.role() == "A") and CHOSE_TO_TAKE:
                expected_payoff += Constants.take_amount - (
                    Constants.deduct["multiplier"] * DEDUCT_AMOUNT
                )
            elif self.player.role() == "B":
                # TODO: Bonus question logic
                expected_payoff = None
            elif (self.player.role() == "C") and CHOSE_TO_TAKE:
                expected_payoff -= Constants.take_amount + DEDUCT_AMOUNT

        if expected_payoff is not None:
            error_message = (
                f"Player: {self.player.role()}, "
                f"Actual Payoff: {self.player.payoff}, "
                f"Expected Payoff: {c(expected_payoff)}"
            )
            assert self.player.payoff == c(expected_payoff), error_message

        yield pages.Feedback

        if self.session.config["rep_condition"] and self.round_number == 2:
            yield pages.CMessage

        if self.round_number == 2 and self.player.role() == "A":
            answers = {
                "ee_a_session": 5,
                "ne_a": 5,
                "ne_a_b_session": 5,
                "ne_a_c_session": 5,
            }

            if CASE != "no_grouping":
                answers = { **answers, "ee_a_group": 5, "ne_a_b_group": 5 }

                if self.session.config["rep_condition"]:
                    answers = { **answers, "ne_a_c_group": 5 }

            yield (pages.BonusQuestions, answers)
