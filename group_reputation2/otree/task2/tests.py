from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
from otree.api import Submission
import random


class PlayerBot(Bot):

    def play_round(self):
        if self.round_number == 1:
            yield Submission(pages.Instructions, check_html=False)
            yield Submission(pages.Instructions2)
            yield Submission(pages.Instructions3, check_html=False)
            yield Submission(pages.Instructions3a, check_html=False)
            yield Submission(pages.Instructions4, check_html=False)

            comp_answers = {'comp1': 1, 'comp2': True, 'comp3': self.session.config['deterrence'], 'comp5': 36, }
            if self.session.config['rep_condition']:
                comp_answers['comp4'] = 2

            yield (pages.Comprehension, comp_answers)

        yield Submission(pages.Commencement, check_html=False)

        if self.player.role() == self.subsession.taking_player:
            yield Submission(pages.Decision, {'chose_to_take': True}, check_html=False)
        elif self.player.role() == self.subsession.deducting_player:
            yield Submission(pages.Decision, {'deduct_amount': 0}, check_html=False)

        yield pages.Feedback

        if self.session.config['rep_condition'] and self.round_number == 2:
            yield pages.CMessage
