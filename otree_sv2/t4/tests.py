from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
import random


class PlayerBot(Bot):

    def play_round(self):
        yield (pages.Main, {'q'+str(i): random.randint(1, 5) for i in range(1, 8)})
