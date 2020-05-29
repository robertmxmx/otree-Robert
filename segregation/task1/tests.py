from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
import random


class PlayerBot(Bot):

    def play_round(self):

        if self.group.at_starting_periods():
            yield (pages.Confirm)
            yield (pages.PayoffAfterMoving)
        else:
            yield (pages.MoveDecision, {'chose_to_switch': random.choice([True, False])})

            yield (pages.PayoffAfterMoving)

            if self.session.config['treatment'] == 1:
                if len(self.participant.vars['town_pop']) != 0:
                    yield (pages.DeductionDecision,
                           {'deduct' + str(p['raw_id']): random.randint(0, 10) for p in self.participant.vars['town_pop']})
                else:
                    yield (pages.DeductionDecision)

                yield (pages.Summary)
