from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
from otree.api import Submission, SubmissionMustFail
import random


class PlayerBot(Bot):
    a_decision = random.randint(1, 11)
    b_decision = [
        random.choice([0, 1]) for i in range(11)
    ]

    def play_round(self):
        yield Submission(pages.Instructions, check_html=False)

        yield (pages.Comprehension1, {'c1a': 0, 'c1b': 0})
        yield (pages.Comprehension2, {'c2a': 8, 'c2b': 4})

        if self.participant.id_in_session % 2:
            yield(pages.ParticipantADecision, {'a_decision': 5})
        else:
            yield(pages.ParticipantBDecision, {
                'b_decision1': 1,
                'b_decision2': 1,
                'b_decision3': 1,
                'b_decision4': 1,
                'b_decision5': 1,
                'b_decision6': 1,
                'b_decision7': 1,
                'b_decision8': 1,
                'b_decision9': 1,
                'b_decision10': 1,
                'b_decision11': 1,
            })

        # if self.participant.id_in_session % 2:
            # assert self.participant.vars['task_payoffs'][0] == c(Constants.total_points - self.a_decision if self.b_decision[self.a_decision-1] else 0)
        # else:
            # assert self.participant.vars['task_payoffs'][0] == c(self.a_decision if self.b_decision[self.a_decision-1] else 0)
        yield(pages.Outcome)
