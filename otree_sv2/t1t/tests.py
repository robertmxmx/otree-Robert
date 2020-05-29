from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
from otree.api import Submission, SubmissionMustFail
import random


class PlayerBot(Bot):

    def play_round(self):

        yield Submission(pages.Instructions, check_html=False)

        yield (pages.Comprehension1, {'c1': 3})

        yield(pages.Comprehension2, {'c2': 4})

        if self.participant.id_in_session % 2:
            yield(pages.ParticipantADecision, {'a_transfer': 3})
        else:
            yield(pages.ParticipantBDecision, {
                'b_transfer1': 1.0,
                'b_transfer2': 0.0,
                'b_transfer3': 1.5, # self.b_transfer[2],
                'b_transfer4': 2.5,
            })

        yield(pages.Outcome)
