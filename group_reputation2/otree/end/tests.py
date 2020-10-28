from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
from otree.api import Submission


class PlayerBot(Bot):

    def play_round(self):
        if 'group' not in self.participant.vars:
            yield Submission(pages.UngroupedEnd, check_html=False)
        else:
            yield Submission(pages.End, check_html=False)
