from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
from otree.api import Submission


class PlayerBot(Bot):

    def play_round(self):
        print(self.html)
        yield (pages.WithoutID, { 'pay_id': 'testinput' })
        yield Submission(pages.WithID, check_html=False)
