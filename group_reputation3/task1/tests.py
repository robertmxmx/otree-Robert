from . import pages
from ._builtin import Bot


# Test cases. Uncomment the specific case to use. NOTE: Remember to use the same
# case in Task 2 tests
CASE = "no_grouping"
# CASE = "group_by_birth"
# CASE = "group_by_politics"

DEFAULT_SURVEY_ANSWERS = {
    "birth_region": 3,
    "pi_q1": 1,
    "pi_q2": 1,
    "pi_q3": 1,
    "pi_q4": 1,
    "pi_q5": 1,
    "pi_q6": 1,
    "pi_q7": 1,
}


class PlayerBot(Bot):
    def play_round(self):
        if CASE == "no_grouping":
            yield (pages.InitialSurvey, DEFAULT_SURVEY_ANSWERS)
        elif CASE == "group_by_birth":
            if self.participant.id_in_session in [1, 5]:
                yield (pages.InitialSurvey, DEFAULT_SURVEY_ANSWERS)
            else:
                yield (
                    pages.InitialSurvey,
                    {**DEFAULT_SURVEY_ANSWERS, "birth_region": 2},
                )
        else:
            if self.participant.id_in_session in [1, 5]:
                yield (
                    pages.InitialSurvey,
                    {**DEFAULT_SURVEY_ANSWERS, "birth_region": 2},
                )
            else:
                yield (
                    pages.InitialSurvey,
                    {
                        **DEFAULT_SURVEY_ANSWERS,
                        "pi_q1": 7,
                        "pi_q2": 7,
                        "pi_q3": 7,
                        "pi_q4": 7,
                        "pi_q5": 7,
                        "pi_q6": 7,
                        "pi_q7": 7,
                    },
                )
