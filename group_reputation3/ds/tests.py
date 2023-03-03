from . import pages
from ._builtin import Bot
import random


class PlayerBot(Bot):
    def play_round(self):
        if "group" not in self.participant.vars:
            return

        answers = {
            "area_of_study": "Physics",
            "supporting_competition": 2,
            "supporting_team": "a team",
            "num_experiments": 2,
            "gender": "Male",
            "similarity1": 2,
            "similarity2": 5,
            "retaliate_def": "idk",
            "retaliate_type": "idk2",
            "retaliate_beh": "idk3",
        }

        if self.player.pi_class():
            answers["pi_classification"] = random.randint(1, 6)

        if self.player.role() == "A" and not self.session.config["deterrence"]:
            answers.update(
                {
                    "BC_from_China": random.randint(1, 6),
                    "BC_from_Malaysia": random.randint(1, 6),
                    "BC_from_Australia": random.randint(1, 6),
                    "BC_from_Singapore": random.randint(1, 6),
                    "BC_from_India": random.randint(1, 6),
                    "BC_from_Hong_Kong": random.randint(1, 6),
                }
            )

        if self.player.role() == "B" or self.player.role() == "C":
            answers.update(
                {
                    "A_from_China": random.randint(1, 6),
                    "A_from_Malaysia": random.randint(1, 6),
                    "A_from_Australia": random.randint(1, 6),
                    "A_from_Singapore": random.randint(1, 6),
                    "A_from_India": random.randint(1, 6),
                    "A_from_Hong_Kong": random.randint(1, 6),
                }
            )

        yield (pages.ExitSurvey, answers)
