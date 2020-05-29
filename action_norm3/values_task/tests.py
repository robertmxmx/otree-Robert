from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
import random


class PlayerBot(Bot):

    def play_round(self):
        yield (pages.Instructions)

        for i in range(Constants.num_sp):
            yield (pages.Main, {'sp%s' % self.player.sp_count: random.choice([1, 2])})

        yield (pages.Instructions2)

        for i in range(Constants.num_sp):
            yield (pages.Main2, {'sp%s_accept' % self.player.sp_accept_count: random.choice([True, False])})
