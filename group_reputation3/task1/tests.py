from . import pages
from ._builtin import Bot
import random
# random.seed(12)

BR1 = { "birth_region": 5 }        
BR2 = { "birth_region": 5 }

PI1 = {
    "pi_q1": 7,
    "pi_q2": 4,
    "pi_q3": 5,
    "pi_q4": 7,
    "pi_q5": 5,
    "pi_q6": 7,
    "pi_q7": 7,
}
PI2 = {
    "pi_q1": 7,
    "pi_q2": 4,
    "pi_q3": 1,
    "pi_q4": 5,
    "pi_q5": 7,
    "pi_q6": 1,
    "pi_q7": 1,
}
PI3 = {
    "pi_q1": 4,
    "pi_q2": 4,
    "pi_q3": 3,
    "pi_q4": 4,
    "pi_q5": 2,
    "pi_q6": 4,
    "pi_q7": 4,
}
PI4 = {
    "pi_q1": 1,
    "pi_q2": 1,
    "pi_q3": 3,
    "pi_q4": 7,
    "pi_q5": 3,
    "pi_q6": 3,
    "pi_q7": 2,
}


# NOTE: This test is not always successful at sorting by what is specifed in
# the below comments. This is due to a combination of oTree sorting bots by
# arrival time and the bots landing on the wait page at indeterminate times.

class PlayerBot(Bot):
    def play_round(self):
        id = self.participant.id_in_session
        inputs = {}
        die = random.randint(1, 10)

        # Sort by random input
        if die == 1:
            inputs = {**BR1, **PI2}
        if die == 2:
            inputs = {**BR2, **PI2}
        if die == 3:
            inputs = {"birth_region": random.randint(2, 13), **PI1}
        if die == 4:
            inputs = {"birth_region": random.randint(2, 13), **PI3}
        if die == 5:
            inputs = {"birth_region": random.randint(5, 7), **PI4}
        if die == 6:
            inputs = {"birth_region": random.randint(4, 9), **PI3}
        if die == 7:
            inputs = {"birth_region": random.randint(1, 7), **PI4}
        if die == 8:
            inputs = {"birth_region": random.randint(4, 12), **PI3}
        if die == 9:
            inputs = {"birth_region": random.randint(4, 7), **PI4}
        if die == 10:
            inputs = {"birth_region": random.randint(6, 7), **PI2}
        # # Sort this group by birth region
        # if id == 1:
        #     inputs = {**BR2, **PI3}
        # elif id in [2, 3]:
        #     inputs = {**BR2, **PI3}
        # # Sort this group by political ideology
        # elif id == 4:
        #     inputs = {**BR2, **PI1}
        # elif id in [5, 6]:
        #     inputs = {**BR2, **PI2}
        # # Sort this group randomly
        # elif id in [7, 8, 9]:
        #     inputs = {**BR2, **PI3}
        # # Also sort this group by birth region. This ensures at least one
        # # gets the extra belief questions
        # if id == 10:
        #     inputs = {**BR1, **PI3}
        # elif id in [11, 12]:
        #     inputs = {**BR2, **PI3}
        # # Use the same inputs for the rest of the bots
        # else:
        #     inputs = {**BR1, **PI1}

        yield (pages.InitialSurvey, inputs)
