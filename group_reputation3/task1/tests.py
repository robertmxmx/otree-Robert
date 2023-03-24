from . import pages
from ._builtin import Bot


BR1 = { "birth_region": 1 }
BR2 = { "birth_region": 2 }

PI1 = {
    "pi_q1": 1,
    "pi_q2": 7,
    "pi_q3": 7,
    "pi_q4": 1,
    "pi_q5": 1,
    "pi_q6": 7,
    "pi_q7": 7,
}
PI2 = {
    "pi_q1": 7,
    "pi_q2": 1,
    "pi_q3": 1,
    "pi_q4": 7,
    "pi_q5": 7,
    "pi_q6": 1,
    "pi_q7": 1,
}
PI3 = {
    "pi_q1": 4,
    "pi_q2": 4,
    "pi_q3": 4,
    "pi_q4": 4,
    "pi_q5": 4,
    "pi_q6": 4,
    "pi_q7": 4,
}


# NOTE: This test is not always successful at sorting by what is specifed in
# the comments. This is due to a combination of oTree sorting bots by arrival
# time and the bots landing on the wait page at indeterminate times.

class PlayerBot(Bot):
    def play_round(self):
        # Sort this group by birth region
        if self.participant.id_in_session == 1:
            yield (pages.InitialSurvey, {**BR1, **PI3})
        elif self.participant.id_in_session in [2, 3]:
            yield (pages.InitialSurvey, {**BR2, **PI3})

        # Sort this group by political ideology
        elif self.participant.id_in_session == 4:
            yield (pages.InitialSurvey, {**BR2, **PI1})
        elif self.participant.id_in_session in [5, 6]:
            yield (pages.InitialSurvey, {**BR2, **PI2})

        # Sort this group randomly
        elif self.participant.id_in_session in [7, 8, 9]:
            yield (pages.InitialSurvey, {**BR2, **PI3})

        # Also sort this group by birth region. This ensures at least one
        # gets the extra belief questions
        if self.participant.id_in_session == 10:
            yield (pages.InitialSurvey, {**BR1, **PI3})
        elif self.participant.id_in_session in [11, 12]:
            yield (pages.InitialSurvey, {**BR2, **PI3})
