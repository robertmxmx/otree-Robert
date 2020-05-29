from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
from otree.api import Submission
import random


class PlayerBot(Bot):

    def play_round(self):

        if self.round_number == 1:
            yield (pages.Start)
            yield Submission(pages.Stage1Instructions, check_html=False)
            yield Submission(pages.Stage2Instructions, check_html=False)
            yield Submission(pages.Stage3Instructions, check_html=False)
            yield (pages.ComprehensionQuestions, Constants.comp_answers)

        # r1_pressed = True
        # r2_pressed = True
        # g1_pressed = False
        # g2_pressed = False
        # d_accepted = True

        r1_pressed = random.choice([True, False])
        r2_pressed = random.choice([True, False])
        g1_pressed = random.choice([True, False])
        g2_pressed = random.choice([True, False])
        d_accepted = random.choice([True, False])

        yield (pages.Beginning)

        # if self.round_number == self.session.config['sp_round_num']:        # fixme
        #     pass
        # else:

        if self.player == self.group.get_player_by_role('r1'):
            yield (pages.Stage1Decision, {'pressed_red': r1_pressed})

        if self.player == self.group.get_player_by_role('r2'):
            yield (pages.Stage1Decision, {'pressed_red': r2_pressed})

        if self.group.num_red_pressed == 2:
            if self.player == self.group.get_player_by_role('g1'):
                yield (pages.Stage2Decision, {'pressed_green': g1_pressed})

            if self.player == self.group.get_player_by_role('g2'):
                yield (pages.Stage2Decision, {'pressed_green': g2_pressed})

        yield (pages.Feedback)

        if self.group.num_red_pressed > 0:
            if self.player == self.group.get_player_by_role('unaff'):
                yield Submission(pages.Stage3Decision, {
                    'red_d_pts': random.randint(0, 10),
                    'green_d_pts': 0 if self.group.num_green_not_pressed == 0 or self.group.num_red_pressed != 2 else random.randint(0, 10)
                }, check_html=False)

            if self.player == self.group.get_player_by_role('aff'):
                if self.group.get_player_by_role('unaff').red_d_pts == \
                        self.group.get_player_by_role('unaff').green_d_pts == 0:
                    yield (pages.Stage3Agreement)
                else:
                    yield (pages.Stage3Agreement, {'accepted_deduction': d_accepted})

            yield (pages.Stage3Feedback)

        if self.round_number == self.session.config['exp_round_num']:
            yield (pages.ExpectationSurvey, {'exp1': 2, 'exp2': 2, 'exp3': 2})
            yield (pages.ExpectationEnd)

        if self.round_number == Constants.num_rounds:
            yield (pages.ExpectationFeedback)
