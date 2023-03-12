from otree.api import Currency as c
from ._builtin import Page


# TODO Move this to end app
QUESTION_NUMBERS = {
    "ee_a_group": 1,
    "ee_a_session": 2,
    "ne_a": 3,
    "ne_a_b_group": 4,
    "ne_a_b_session": 5,
    "ne_a_c_group": 6,
    "ne_a_c_session": 7,
    "ee_b_group": 1,
    "ee_b_session": 2,
    "ne_b": 3,
    "ne_b_b_group": 4,
    "ne_b_b_session": 5,
    "ne_b_c_group": 6,
    "ne_b_c_session": 7,
    "ee_c_group": 1,
    "ee_c_session": 2,
    "ne_c": 3,
    "ne_c_c_group": 4,
    "ne_c_c_session": 5,
}


def to_aud(amount, session):
    if amount is None:
        return None

    return c(amount).to_real_world_currency(session)


class End(Page):
    def is_displayed(self):
        return (
            not self.participant.vars["droppedout"] and "group" in self.participant.vars
        )

    def vars_for_template(self):
        session = self.session
        totalpayoff = 0
        p_vars = self.participant.vars

        chosen_task = session.config["chosen_task"]

        task_payoff = p_vars["task_payoffs"][chosen_task - 1]
        totalpayoff += task_payoff

        belief_bonus = p_vars["belief_bonus"]
        if belief_bonus["paid"]:
            totalpayoff += belief_bonus["amount"]

        if "survey_bonus" in p_vars:
            survey_bonus = p_vars["survey_bonus"]
            totalpayoff += survey_bonus

        self.participant.payoff = c(totalpayoff)
        self.player.final_payoff = float(to_aud(totalpayoff, session))

        return {
            "belief_bonus": {
                **belief_bonus,
                "amount": to_aud(belief_bonus["amount"], session),
                "question": QUESTION_NUMBERS[belief_bonus["question"]],
            },
            "chosen_task": chosen_task,
            "participation_fee": session.config["participation_fee"],
            "role": p_vars["role"],
            "survey_bonus": to_aud(survey_bonus, session),
            "task_payoff": to_aud(task_payoff, session),
        }


class UngroupedEnd(Page):
    def is_displayed(self):
        return (
            not self.participant.vars["droppedout"]
            and "group" not in self.participant.vars
        )


page_sequence = [End, UngroupedEnd]
