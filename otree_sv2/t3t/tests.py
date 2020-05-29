from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
import random


class PlayerBot(Bot):

    def play_round(self):
        if self.participant.id_in_session % 2:
            yield(pages.ParticipantADecision, {'a_transfer': 3})
        else:
            yield(pages.ParticipantBDecision, {
                'b_transfer1': 2.0,
                'b_transfer2': 2.0,
                'b_transfer3': 1.5,
                'b_transfer4': 4.5,
            })

        yield(pages.Outcome)

        if self.participant.id_in_session % 2:
            yield(pages.Survey, {'survey_qa1': 4})
        else:
            yield(pages.Survey, {'survey_qb1': '3'})
