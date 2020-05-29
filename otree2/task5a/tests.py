from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):

    def play_round(self):
        if self.player.id_in_group == 1:
            yield (pages.Participant1, {'p1_sent': 0})
        else:
            yield (pages.Participant2, {'p2_sent': 0})
        yield (pages.Outcome)
        if self.round_number == Constants.num_rounds:
            yield (pages.Survey, {"survey_q1": 1, "survey_q2": "test_input"})
            yield (pages.End)