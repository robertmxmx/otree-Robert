from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
import random


class PlayerBot(Bot):

    def play_round(self):
        if self.round_number == 1:
            yield (pages.Instructions)
            yield (pages.DetailedInstructions)

        yield (pages.MoveDecision, {'chose_to_switch': random.choice([True, False])})

        yield (pages.PayoffAfterMoving)