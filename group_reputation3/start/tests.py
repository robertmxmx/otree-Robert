from . import pages
from ._builtin import Bot
from otree.api import Submission


class PlayerBot(Bot):
    def play_round(self):
        yield (pages.Consent, {"accept": True})
        yield Submission(pages.Welcome, check_html=False)

        if self.session.config["online_exp"]:
            yield Submission(pages.InternetRequirement, check_html=False)
