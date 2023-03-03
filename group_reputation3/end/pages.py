from otree.api import Currency as c
from ._builtin import Page


def to_aud(amount, page):
    return (
        c(amount).to_real_world_currency(page.session) if amount is not None else None
    )


class End(Page):
    def is_displayed(self):
        return (
            not self.participant.vars["droppedout"] and "group" in self.participant.vars
        )

    def vars_for_template(self):
        totalpayoff = 0
        bonus = None
        p_vars = self.participant.vars

        chosen_task = self.session.config["chosen_task"]
        chosen_task_name = f"task{chosen_task}"

        task2_payoff = p_vars["task2_payoffs"][chosen_task - 1]
        totalpayoff += task2_payoff

        if "bonuses" in p_vars:
            bonus = p_vars["bonuses"]["task1"] + p_vars["bonuses"]["task2"]
            totalpayoff += bonus

        if "survey_bonus" in p_vars:
            surveybonus = p_vars["survey_bonus"]
            totalpayoff += surveybonus

        self.participant.payoff = c(totalpayoff)
        self.player.final_payoff = float(to_aud(totalpayoff, self))

        show_guess_feedback = ((chosen_task == 1) and (p_vars["role"] == "C")) or (
            (chosen_task == 2) and (p_vars["role"] == "B")
        )

        return {
            "bonus": to_aud(bonus, self) if bonus else None,
            "chosen_task": chosen_task,
            "correctly_guessed": p_vars["bonuses"][chosen_task_name] > 0,
            "deducting_player": p_vars["deducting_players"][chosen_task_name],
            "participation_fee": self.session.config["participation_fee"],
            "role": p_vars["role"],
            "show_guess_feedback": show_guess_feedback,
            "survey_bonus": to_aud(surveybonus, self),
            "task2_payoff": to_aud(task2_payoff, self),
        }


class UngroupedEnd(Page):
    def is_displayed(self):
        return (
            not self.participant.vars["droppedout"]
            and "group" not in self.participant.vars
        )


page_sequence = [End, UngroupedEnd]
