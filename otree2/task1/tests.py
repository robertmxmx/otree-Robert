from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
from otree.api import Submission


class PlayerBot(Bot):

    def play_round(self):
        if self.round_number == 1:
            yield Submission(pages.Instructions, check_html=False)
            yield (pages.Comprehension, {'comp1': "-2 points"})
            yield (pages.Comprehension2, {'comp2': "Play DEFER"})
        if self.player.id_in_group == 1:
            yield (pages.Role1, {'r1_action': "CHALLENGE"})
        else:
            yield (pages.Role2, {'r2_action': "RETALIATE"})
        yield (pages.Outcome)
        if self.round_number == Constants.num_rounds:
            yield (pages.End)
