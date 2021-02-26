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
            # i = self.html.find("bonus")
            # bonus_text = self.html[i-10:i+30] if i != -1 else ""
            # print("Player: %s - %s" % (self.player.participant.vars['role'], bonus_text))

            yield Submission(pages.End, check_html=False)
