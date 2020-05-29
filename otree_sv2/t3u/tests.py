from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
import random


class PlayerBot(Bot):
    a_decision = random.randint(1, 11)
    b_decision = [
        random.choice([0, 1]) for i in range(11)
    ]

    def play_round(self):
        if self.participant.id_in_session % 2:
            yield(pages.ParticipantADecision, {'a_decision': 10}) # self.a_decision})
        else:
            yield(pages.ParticipantBDecision, {
                'b_decision1': 0, # self.b_decision[0],
                'b_decision2': 0, # self.b_decision[1],
                'b_decision3': 0, # self.b_decision[2],
                'b_decision4': 0, # self.b_decision[3],
                'b_decision5': 0, # self.b_decision[4],
                'b_decision6': 0, # self.b_decision[5],
                'b_decision7': 0, # self.b_decision[6],
                'b_decision8': 0, # self.b_decision[7],
                'b_decision9': 0, # self.b_decision[8],
                'b_decision10': 0, # self.b_decision[9],
                'b_decision11': 0, # self.b_decision[10],
            })

        # if self.participant.id_in_session % 2:
            # assert self.participant.vars['task_payoffs'][2] == c(Constants.total_points - self.a_decision if self.b_decision[self.a_decision-1] else 0)
        # else:
            # assert self.participant.vars['task_payoffs'][2] == c(self.a_decision if self.b_decision[self.a_decision-1] else 0)
        yield(pages.Outcome)

        if self.participant.id_in_session % 2:
            yield(pages.Survey, {'survey_qa1': 4})
        else:
            yield(pages.Survey, {'survey_qb1': 3})
