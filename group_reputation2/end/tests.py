from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
from otree.api import Submission


class PlayerBot(Bot):

    def play_round(self):
        # i = self.html.index('Your total earnings are')
        # print(self.html[i:i+200])
        yield Submission(pages.Main, check_html=False)
