from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
from otree.api import Submission
import random


class PlayerBot(Bot):

    def play_round(self):
        # r1_pressed = True
        # r2_pressed = True
        # g_pressed = False
        # d_accepted = True

        r1_pressed = random.choice([True, False])
        r2_pressed = random.choice([True, False])
        g_pressed = random.choice([True, False])
        d_accepted = random.choice([True, False])

        yield (pages.Beginning)

        if self.round_number == self.session.config['sp_round_num']:
            yield Submission(pages.SpecialRoundInstructions, check_html=False)
            yield (pages.SpecialRound, {
                'sp_pressed_red': random.choice([True, False]),
                'sp_pressed_green': random.choice([True, False]),
                'sp_unaff_1r': random.randint(1, 2),
                'sp_unaff_2r1g': random.randint(1, 2),
                'sp_unaff_2r0g': random.randint(1, 4),
                'sp_aff_1r': random.randint(1, 2),
                'sp_aff_2r1g': random.randint(1, 2),
                'sp_aff_2r0g': random.randint(1, 6)
            })

            if self.group.num_red_pressed == 0:
                yield (pages.Feedback)
            else:
                yield (pages.Stage3Feedback)

        else:
            if self.player == self.group.get_player_by_role('red_presser1'):
                yield (pages.Stage1Decision, {'pressed_red': r1_pressed})

            if self.player == self.group.get_player_by_role('red_presser2'):
                yield (pages.Stage1Decision, {'pressed_red': r2_pressed})

            if self.group.num_red_pressed == 2 and self.player == self.group.get_player_by_role('green_presser'):
                yield (pages.Stage2Decision, {'pressed_green': g_pressed})

            yield (pages.Feedback)

            if self.group.num_red_pressed > 0:
                if self.player == self.group.get_player_by_role('unaffected'):
                    yield Submission(pages.Stage3Decision, {
                        'red_d_pts': random.randint(0, 10),
                        'green_d_pts': 0 if self.group.get_player_by_role(
                            'green_presser').pressed_green or self.group.num_red_pressed != 2 else random.randint(0,
                                                                                                                  10)
                    }, check_html=False)

                if self.player == self.group.get_player_by_role('affected'):
                    if self.group.get_player_by_role('unaffected').red_d_pts == \
                            self.group.get_player_by_role('unaffected').green_d_pts == 0:
                        yield (pages.Stage3Agreement)
                    else:
                        yield (pages.Stage3Agreement, {'accepted_deduction': d_accepted})

                yield (pages.Stage3Feedback)

        if self.round_number == self.session.config['exp_round_num']:
            yield (pages.ExpectationSurvey, {'exp1': 2, 'exp2': 2, 'exp3': 2})
            yield (pages.ExpectationEnd)

        if self.round_number == Constants.num_rounds:
            yield (pages.ExpectationFeedback)
