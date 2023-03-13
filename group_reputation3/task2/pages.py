from ._builtin import Page, WaitPage
from .models import Constants

from _myshared.constants import REGIONS, SortTypes


def create_html_table(d):
    content = "<table class='simple-table'><tr>"

    for key, value in dict(sorted(d.items())).items():
        content += f"<th>{key}</th>"

    content += "</tr><tr>"

    for key, value in dict(sorted(d.items())).items():
        content += f"<td>{value}</td>"

    content += "</tr></table>"

    return content


def get_group_sort(player, group):
    """
    Returns text that describes how the group was sorted. Can be:
    - Politically Conservative/Progressive
    - From <REGION>
    - None if sorted randomly
    """
    sorted_by = player.participant.vars["sorted_by"]

    if sorted_by == SortTypes.NONE.value:
        return None

    # Could also use player B as they have the same birth region/ideology
    player_C = group.get_player_by_role("C")

    if sorted_by == SortTypes.BIRTH_REGION.value:
        return f"from {REGIONS[player_C.br - 1]}"
    elif sorted_by == SortTypes.POLITICAL_IDEOLOGY.value:
        return (
            "politically progressive"
            if player_C.pi == 1
            else "politically conservative"
        )


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

        return "The following questions are incorrect: " + ", ".join(incorrectqnums)


class Commencement(Page):
    pass


class TakingDecision(Page):
    form_model = "player"
    form_fields = ["chose_to_take"]

    def is_displayed(self):
        return self.player.role() == self.subsession.taking_player

    def vars_for_template(self):
        chose_to_take_label = (
            f"Do you wish to take {Constants.take_amount} of "
            f"{self.subsession.deducting_player}'s ECU?"
        )

        return {
            **self.player.get_instruction_vars(),
            "show_init_msg": False,
            "chose_to_take_label": chose_to_take_label,
            "revealed": False,
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
            "revealed": False,
        }


class BonusQuestions(Page):
    """Page where B/C are asked questions during Task 1/2"""

    form_model = "player"

    def is_displayed(self):
        return self.round_number == 1

    def get_form_fields(self):
        similar_groups_exist = len(self.group.get_similar_groups()) > 0
        reputation_treatment = self.session.config["rep_condition"]
        fields = []

        if self.player.role() == "A":
            fields.extend(
                [
                    "ee_a_session",
                    "ne_a",
                    "ne_a_b_session",
                    "ne_a_c_session",
                ]
            )

            if similar_groups_exist:
                fields.extend(["ee_a_group", "ne_a_b_group"])

                if reputation_treatment:
                    fields.extend(["ne_a_c_group"])
        elif self.player.role() == "B":
            fields.extend(["ee_b_session", "ne_b", "ne_b_b_session", "ne_b_c_session"])

            if similar_groups_exist:
                fields.extend(["ee_b_group", "ne_b_b_group"])

                if reputation_treatment:
                    fields.extend(["ne_b_c_group"])
        elif self.player.role() == "C":
            fields.extend(["ee_c_session", "ne_c", "ne_c_c_session"])

            if reputation_treatment and similar_groups_exist:
                fields.extend(["ee_c_group", "ne_c_c_group"])

        return fields

    def vars_for_template(self):
        similar_groups = self.group.get_similar_groups()

        if len(similar_groups) == 0:
            return {"same_group_sort": None}

        return {"same_group_sort": get_group_sort(self.player, self.group)}


class CalculatePayoffs(WaitPage):
    wait_for_all_groups = True

    def after_all_players_arrive(self):
        for group in self.subsession.get_groups():
            group.set_payoffs()


class Feedback(Page):
    def get_payoffs(self, final=False):
        other_player_role = "C" if self.round_number == 1 else "B"
        payoffs = {}

        for p in self.group.get_players():
            role = p.role()
            payoffs[role] = (
                int(p.participant.payoff) if final else int(p.payoff_after_take)
            )

            # Show inital payoff of other player. This prevents adding in any
            # bonus amounts the player earned (for correctly guessing how much
            # ECU the other players spent)
            if role == other_player_role:
                payoffs[role] = Constants.initial_payoffs[role]

        return dict(sorted(payoffs.items()))

    def get_vars(self, round_num):
        player_A = self.group.get_player_by_role("A").in_round(round_num)
        deducting_player_role = "B" if round_num == 1 else "C"
        deducting_player = self.group.get_player_by_role(
            deducting_player_role
        ).in_round(round_num)

        deduct_amount = int(deducting_player.deduct_amount)
        amount_reduced = int(Constants.deduct["multiplier"] * deduct_amount)

        return {
            "chose_to_take": player_A.chose_to_take,
            "deducting_player": deducting_player_role,
            "payoffs_after_take": self.get_payoffs(),
            "deduct_amount": deduct_amount,
            "amount_reduced": amount_reduced,
            "final_payoffs": self.get_payoffs(True),
        }

    def vars_for_template(self):
        round1_vars = self.get_vars(round_num=1)

        if self.round_number == 1:
            return {"round1": round1_vars}
        else:
            return {
                "round1": round1_vars,
                "round2": {
                    **self.get_vars(round_num=2),
                    "receiving_info": self.player.role() in ["A", "C"],
                },
            }

    def before_next_page(self):
        p = self.participant

        if "task_payoffs" not in p.vars:
            p.vars["task_payoffs"] = []

        p.vars["task_payoffs"].append(p.payoff)


class CMessage(Page):
    def is_displayed(self):
        return self.session.config["rep_condition"] and self.round_number == 2

    def vars_for_template(self):
        return {
            **self.player.get_instruction_vars(),
            "show_init_msg": False,
            "revealed": True,
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
    BonusQuestions,
    CalculatePayoffs,
    Feedback,
    CMessage,
]
