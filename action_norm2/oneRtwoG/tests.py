from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
from otree.api import Submission, SubmissionMustFail
import random


class PlayerBot(Bot):

    def play_round(self):

        yield (pages.Beginning)

        if self.round_number != Constants.sp_round_num:
            if self.player.player_id == self.group.r_presser:
                yield (pages.Stage1Decision, {'r_pressed': True})

            if self.group.r_pressed:
                if self.player.player_id == self.group.g1_presser:
                    yield (pages.Stage2Decision, {'g1_pressed': True})

                if self.player.player_id == self.group.g2_presser:
                    yield (pages.Stage2Decision, {'g2_pressed': False})

                yield (pages.Stage2Feedback)

                if self.player.player_id == self.group.unaffected:
                    yield (pages.Stage3Decision, {
                        'r_deduction_pts': 20,
                        'g_deduction_pts': 10
                    })

                if self.player.player_id == self.group.r_affected:
                    yield Submission(pages.Stage3Agreement, {'deduction_accepted': True}, check_html=False)

                yield (pages.Feedback)
            else:
                yield (pages.Stage2Feedback)

        else:

            yield (pages.SpecialRound, {
                'r_pressed': True, 'g_pressed': True, 'd_un_r0g': 1, 'd_un_r1g': 1, 'd_un_r2g': 1, 'd_aff_r0g': 1,
                'd_aff_r1g': 1, 'd_aff_r2g': 1
            })
            yield (pages.Feedback)
