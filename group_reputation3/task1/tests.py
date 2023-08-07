import random

from _myshared.constants import REGIONS
from . import pages
from ._builtin import Bot


BR1 = {"birth_region": 1}
BR2 = {"birth_region": 2}

PI = {
    "pi_q1": 4,
    "pi_q2": 4,
    "pi_q3": 4,
    "pi_q4": 4,
    "pi_q5": 4,
    "pi_q6": 4,
    "pi_q7": 4,
}


def random_pi_answers():
    return {
        "pi_q1": random.randint(1, 7),
        "pi_q2": random.randint(1, 7),
        "pi_q3": random.randint(1, 7),
        "pi_q4": random.randint(1, 7),
        "pi_q5": random.randint(1, 7),
        "pi_q6": random.randint(1, 7),
        "pi_q7": random.randint(1, 7),
    }


# NOTE: This test is not always successful at sorting by what is specifed in
# the below comments. This is due to a combination of oTree sorting bots by
# arrival time, the bots landing on the wait page at indeterminate times and
# the randomness that political ideology sorting has inbuilt.


class PlayerBot(Bot):
    def play_round(self):
        id = self.participant.id_in_session
        inputs = {}

        # Sort the first group by birth region. Birth region of 4 needs to be
        # set so BR threshold does not overwrite.
        if id == 1:
            inputs = {**BR1, **PI}
        elif id in [2, 3, 4]:
            inputs = {**BR2, **PI}
        # Sort the rest randomly
        else:
            birth_region = random.randint(3, len(REGIONS) - 1)
            inputs = {"birth_region": birth_region, **random_pi_answers()}

        yield (pages.InitialSurvey, inputs)
