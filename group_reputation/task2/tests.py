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
            yield Submission(pages.Instructions4, check_html=False)
            if self.session.config['stage2_active']:
                yield (pages.Comprehension, {'comp1': 2, 'comp2': True, 'comp3': 36})
            else:
                yield (pages.Comprehension, {'comp1': 1, 'comp3': 36})

        if self.round_number == 1 or \
                self.round_number == 2 and self.session.config['stage2_active']:
            if self.player.role() == self.subsession.taking_player:
                yield Submission(pages.Decision, {'chose_to_take': True}, check_html=False)
                # yield Submission(pages.Decision, {'chose_to_take': random.choices([True, False])}, check_html=False)
            elif self.player.role() == self.subsession.deducting_player:
                yield Submission(pages.Decision, {'deduct_amount': 0}, check_html=False)
                # yield Submission(pages.Decision, {'deduct_amount': random.randint(Constants.deduct['min'], Constants.deduct['max'])}, check_html=False)
            yield (pages.Feedback)
