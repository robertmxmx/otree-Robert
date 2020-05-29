from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
from otree.api import Submission, SubmissionMustFail


class PlayerBot(Bot):

    def play_round(self):
        if self.subsession.get_task_number() == 2:
            yield Submission(pages.Hold, check_html=False)
        yield (pages.Start)
        yield Submission(pages.Stage1Instructions, check_html=False)
        yield Submission(pages.Stage2Instructions, check_html=False)
        yield Submission(pages.Stage3Instructions, check_html=False)
        yield (pages.ComprehensionQuestions, Constants.comp_answers)
