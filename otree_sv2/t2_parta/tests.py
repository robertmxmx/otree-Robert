from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
from otree.api import Submission
import random


class PlayerBot(Bot):

    def play_round(self):
        yield Submission(pages.Instructions, check_html=False)
        for i in range(Constants.num_sp):
            yield (pages.Main, {'sp'+str(self.session.vars['s_order'][self.player.sp_count-1]): 1})
