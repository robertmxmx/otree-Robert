from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


def create_html_table(d):
    content = "<table class='simple-table'><tr>"

    for key, value in dict(sorted(d.items())).items():
        content += f"<th>{key}</th>"

    content += "</tr><tr>"

    for key, value in dict(sorted(d.items())).items():
        content += f"<td>{value}</td>"
        
    content += "</tr></table>"

    return content

class Setup(WaitPage):
    group_by_arrival_time = True
    
    def after_all_players_arrive(self):
        self.group.init_round()


class Instructions(Page):

    def is_displayed(self):
        return self.round_number == 1


class Instructions2(Page):

    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {
            **self.player.get_instruction_vars(),
            "show_init_msg": True,
            "revealed": False,
        }


class VideoInstructions(Page):

    def is_displayed(self):
        return self.round_number == 1


class Instructions3(Page):

    def is_displayed(self):
        return self.round_number == 1


class Instructions3a(Page):

    def is_displayed(self):
        return self.round_number == 1


class Instructions4(Page):

    def is_displayed(self):
        return self.round_number == 1


class Comprehension(Page):
    form_model = "player"

    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {
            **self.player.get_instruction_vars(),
            "show_init_msg": True,
            "revealed": False,
        }

    def get_form_fields(self):
        if self.session.config["rep_condition"]:
            return ["comp1", "comp2", "comp3", "comp4", "comp5"]
        else:
            return ["comp1", "comp2", "comp3", "comp5"]

    def error_message(self, values):
        incorrectqnums = []

        if values["comp1"] != 1:
            incorrectqnums.append("1")
            self.player.comp1_wrong += 1

        if values["comp2"] is not True:
            incorrectqnums.append("2")
            self.player.comp2_wrong += 1

        if self.session.config["deterrence"] != values["comp3"]:
            incorrectqnums.append("3")
            self.player.comp3_wrong += 1

        if self.session.config["rep_condition"] and values["comp4"] != 2:
            incorrectqnums.append("4")
            self.player.comp4_wrong += 1

        if values["comp5"] != 36:
            incorrectqnums.append("5")
            self.player.comp5_wrong += 1

        if len(incorrectqnums) == 0:
            return

        return (
            "The following questions are incorrect: " +
            ", ".join(incorrectqnums)
        )


class Commencement(Page):
    pass


class TakingDecision(Page):
    form_model = "player"
    form_fields = ["chose_to_take"]

    def is_displayed(self):
        return self.player.role() == self.subsession.taking_player

    def vars_for_template(self):
        chose_to_take_label = (
            f"Do you with to take {Constants.take_amount} of "
            f"{self.subsession.deducting_player}'s ECU?"
        )

        return {
            **self.player.get_instruction_vars(),
            "show_init_msg": False,
            "chose_to_take_label": chose_to_take_label,
            "revealed": False
        }


class DeductingDecision(Page):
    form_model = "player"
    form_fields = ["deduct_amount"]

    def is_displayed(self):
        return self.player.role() == self.subsession.deducting_player

    def vars_for_template(self):
        return {
            **self.player.get_instruction_vars(),
            "show_init_msg": False,
            "taking_player": self.subsession.taking_player,
            "revealed": False
        }


class WaitingDecision(Page):
    form_model = "player"
    
    def is_displayed(self):
        active_players = [
            self.subsession.taking_player,
            self.subsession.deducting_player
        ]

        return self.player.role() not in active_players

    def get_form_fields(self):
        if self.round_number == 1:
            return ["will_spend", "should_spend"]
        else:
            return ["should_spend_guess"]


class CalculatePayoffs(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_payoffs()


class Feedback(Page):

    def _get_payoffs(self, final=False):
        other_player_role = "C" if self.round_number == 1 else "B"
        payoffs = {}

        for p in self.group.get_players():
            role = p.role()
            payoffs[role] = (
                int(p.participant.payoff)
                if final
                else int(p.payoff_after_take)
            )

            # Show inital payoff of other player. This prevents adding in any
            # bonus amounts the player earned (for correctly guessing how much
            # ECU the other players spent)
            if role == other_player_role:
                payoffs[role] = Constants.initial_payoffs[role]

        return payoffs

    def vars_for_template(self):
        pat = self._get_payoffs()
        fp = self._get_payoffs(True)
        tp = self.subsession.taking_player
        dp = self.subsession.deducting_player
        ecu_taken = self.group.get_player_by_role(tp).chose_to_take
        da = int(self.group.get_player_by_role(dp).deduct_amount)
        mult_da = int(Constants.deduct["multiplier"] * da)

        if self.round_number == 1:
            # Set feedback content. This is done here so that it can be
            # retrieved in the next round.
            ta = Constants.take_amount
            content = ""

            if ecu_taken:
                content += f"<p>{tp} decided to take {ta} ECU from {dp}</p>"
            else:
                content += f"<p>{tp} decided not to take {ta} ECU from {dp}</p>"

            content += (
                "<p>This led to the following distribution of endowments:</p>"
            )

            content += create_html_table(pat)

            if ecu_taken:
                content += (
                    f"<p>{dp} chose to spend {da} ECU on deductions. This had "
                    f"the effect of reducing {tp}'s endowment by {mult_da} "
                    f"ECU, and reducing {dp}'s endowment by {da} ECU"
                )

            content += "<p>Final earnings for this task are:</p>"
            content += create_html_table(fp)

            self.participant.vars["task2a_feedback"] = content

            return {"task2a_feedback": content}

        return {
            "task2a_feedback": self.participant.vars["task2a_feedback"],
            "receiving_info": self.player.role() in [tp, dp],
            "points_were_taken": ecu_taken,
            "taking_player": tp,
            "deducting_player": dp,
            "payoffs_after_take": dict(sorted(pat.items())),
            "deduct_amount": da,
            "multiplied_deduct_amount": mult_da,
            "final_payoffs": dict(sorted(fp.items()))
        }

    def before_next_page(self):
        p = self.participant

        if "task2_payoffs" not in p.vars:
            p.vars["task2_payoffs"] = []

        p.vars["task2_payoffs"].append(p.payoff)

        if "deducting_players" not in p.vars:
            p.vars["deducting_players"] = {"task1": None, "task2": None}

        current_task = "task1" if self.round_number == 1 else "task2"
        deducting_player = self.subsession.deducting_player

        p.vars["deducting_players"][current_task] = deducting_player

class CMessage(Page):

    def is_displayed(self):
        return self.session.config["rep_condition"] and self.round_number == 2
    
    def vars_for_template(self):
        return {
            **self.player.get_instruction_vars(),
            "show_init_msg": False,
            "revealed": True
        }
    

page_sequence = [
    Setup,

    Instructions,
    Instructions2,
    VideoInstructions,
    Instructions3,
    Instructions3a,
    Instructions4,

    Comprehension,

    Commencement,

    TakingDecision,
    DeductingDecision,
    WaitingDecision,

    CalculatePayoffs,
    Feedback,

    CMessage
]
