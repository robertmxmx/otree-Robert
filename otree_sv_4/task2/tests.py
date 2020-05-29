from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
from otree.api import Submission
import random


class PlayerBot(Bot):
    def play_round(self):
        partb_options = [ 
            str(_) for _ in range(Constants.min_bid, Constants.max_bid + 1) 
        ] + [ 'out' ]

        yield Submission(pages.PartAInstructions, check_html=False)

        for i in range(len(Constants.statements)):
            statement = self.player.get_current_statement()
            yield (pages.PartA, { statement: random.choice([1, 2]) })

        yield Submission(pages.PartBInstructions, check_html=False)

        for i in range(len(Constants.statements)):
            statement = self.player.get_current_statement()
            yield (pages.PartB, { statement + "_bid": random.choice(partb_options) })

        yield pages.PartBOutcome