from otree.api import Currency as c
from ._builtin import Page, WaitPage
from .models import Constants
import random, math

from _myshared.constants import LOW_PERC, HIGH_PERC, SortTypes
from _myshared.output import print_groups
from _myshared.grouping import create_random_groups
from shared import set_reduced_br, create_groups, set_roles


class InitialSurvey(Page):
    form_model = "player"
    form_fields = [
        "birth_region",
        "other_br",
        "pi_q1",
        "pi_q2",
        "pi_q3",
        "pi_q4",
        "pi_q5",
        "pi_q6",
        "pi_q7",
    ]

    def vars_for_template(self):
        money_per_point = self.session.config["real_world_currency_per_point"]
        bonus = c(Constants.survey_bonus / money_per_point).to_real_world_currency(
            self.session
        )

        return {"survey_bonus": bonus}

    def error_message(self, values):
        if values["birth_region"] == Constants.br_info["other_val"] and (
            values["other_br"] is None or values["other_br"] == ""
        ):
            return "Other birth region was selected but not specified"

    def before_next_page(self):
        money_per_point = self.session.config["real_world_currency_per_point"]
        self.player.participant.vars["survey_bonus"] = (
            Constants.survey_bonus / money_per_point
        )


class FormGroups(WaitPage):
    wait_for_all_groups = True

    def after_all_players_arrive(self):
        # Find the political ideology of players
        scores = []
        valid_players = []

        for p in self.subsession.get_players():
            all_pi_questions = (
                p.pi_q1,
                p.pi_q2,
                p.pi_q3,
                p.pi_q4,
                p.pi_q5,
                p.pi_q6,
                p.pi_q7,
            )

            if p.participant.vars["droppedout"] or None in all_pi_questions:
                continue

            p.set_pi_score()
            scores.append(p.pi_score)
            valid_players.append(p)

        scores.sort()

        # Subjects are categorised by political ideology. Those with highest
        # scores are coded 1 and those with lowest scores 3, with neutrals as 2.
        # Thresholds are defined in /shared.py lines 2 and 3. Ideology groups
        # will not be formed based on shared neutral ideology. For example:
        # if there are two 2's and one 1 then they will be in the no group
        # condition.
        low_per = scores[math.ceil(LOW_PERC * len(scores)) - 1]
        high_per = scores[math.ceil(HIGH_PERC * len(scores)) - 1]

        for p in valid_players:
            if p.pi_score >= high_per:
                p.pol_ideology = 1
            elif p.pi_score <= low_per:
                p.pol_ideology = 3
            else:
                p.pol_ideology = 2

        # Contains players that are still left to sort
        players = []

        for p in valid_players:
            players.append(
                {
                    "id": p.participant.id_in_session,
                    "birth_region": p.birth_region,
                    "pol_ideology": p.pol_ideology,
                }
            )

        # For the regions that have number of players that are less than
        # BR_THRESHOLD, set them to the other type
        BR_THRESHOLD = 3

        br_info = Constants.br_info
        other_br = br_info["other_val"]
        players = set_reduced_br(players.copy(), BR_THRESHOLD, other_br)
        random.shuffle(players)

        group_limit = Constants.players_per_group

        # Sort players based on birth region
        new_groups, players = create_groups(players.copy(), br_info, group_limit)
        final_groups = set_roles(
            new_groups.copy(), SortTypes.BIRTH_REGION.value, group_limit
        )
        random.shuffle(players)

        pi_info = Constants.pi_info

        # Sort players based on political ideology
        new_groups, players = create_groups(players.copy(), pi_info, group_limit)
        final_groups = final_groups + set_roles(
            new_groups.copy(), SortTypes.POLITICAL_IDEOLOGY.value, group_limit
        )
        random.shuffle(players)

        # Randomly group the rest of the players
        new_groups = create_random_groups(players.copy(), group_limit)
        final_groups = final_groups + set_roles(new_groups.copy(), None, group_limit)

        # Set participant data so that this is shared across apps (tasks)
        for i in range(len(final_groups)):
            for p in final_groups[i]:
                for player in valid_players:
                    if player.participant.id_in_session == p["id"]:
                        player.rl = p["role"]
                        player.sorted_by = p["sorted_by"]

                        player.participant.vars.update(
                            {
                                "group": i,
                                "role": p["role"],
                                "sorted_by": p["sorted_by"],
                                "birth_region": p["birth_region"],
                                "pol_ideology": p["pol_ideology"],
                            }
                        )

        print_groups(final_groups)

    def app_after_this_page(self, upcoming_apps):
        if "group" not in self.participant.vars:
            return "end"


page_sequence = [
    InitialSurvey,
    FormGroups,
]
