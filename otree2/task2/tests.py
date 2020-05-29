from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
from otree.api import Submission


class PlayerBot(Bot):

    def play_round(self):
        if self.round_number == 1:
            yield Submission(pages.Instructions, check_html=False)
            yield (pages.Comprehension, {'comp1': "3 points"})
            yield (pages.Comprehension2, {'comp2': "Participant 2 can send back any amount of points from 0 to 3"})
        if self.player.id_in_group == 1:
            yield (pages.Participant1, {'p1_sent': 0})
        else:
            yield (pages.Participant2, {'p2_sent': 0})
        yield (pages.Outcome)
        if self.round_number == Constants.num_rounds:
            yield (pages.End)