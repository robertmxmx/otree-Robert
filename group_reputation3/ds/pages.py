import os

from ._builtin import Page


class ExitSurvey(Page):
    form_model = "player"

    def get_form_fields(self):
        fields = [
            "area_of_study",
            "supporting_competition",
            "supporting_team",
            "num_experiments",
            "gender",
            "similarity1",
            "similarity2",
            "retaliate_def",
            "retaliate_type",
            "retaliate_beh",
        ]
        if self.player.pi_class():
            fields += ["pi_classification"]
        # set respective fields for players
        if self.player.role() == "A" and not self.session.config["deterrence"]:
            fields += [
                "BC_from_China",
                "BC_from_Malaysia",
                "BC_from_Australia",
                "BC_from_Singapore",
                "BC_from_India",
                "BC_from_Hong_Kong",
            ]
        if self.player.role() == "B" or self.player.role() == "C":
            fields += [
                "A_from_China",
                "A_from_Malaysia",
                "A_from_Australia",
                "A_from_Singapore",
                "A_from_India",
                "A_from_Hong_Kong",
            ]
        return fields

    def vars_for_template(self):
        roles = ["A", "B", "C"]
        roles.pop(roles.index(self.participant.vars["role"]))
        # set relationship question vars
        return {
            "rel_ques_roles": [_ for _ in roles],
            "img_paths": ["self_other" + str(i) + ".png" for i in range(1, 7 + 1)],
        }

    def error_message(self, values):
        if values["supporting_competition"] != 4 and (
            values["supporting_team"] is None or values["supporting_team"] == ""
        ):
            return "A competition was selected but a team was not specified"

if os.environ.get("DEV_SKIP_PAGES", "0") == "1":
    page_sequence = []
else:
    page_sequence = [ExitSurvey]
