from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
import random


class PlayerBot(Bot):

    def play_round(self):
        answers = {
            'area_of_study': 'Physics',
            'supporting_competition': 2,
            'supporting_team': 'a team',
            'num_experiments': 2,
            'gender': 'Male',
            'similarity1': 2,
            'similarity2': 5
        }

        if self.player.role() == 'A' and not self.session.config['knowledge']:
            answers.update({
                'BC_from_China': random.randint(1, 6),
                'BC_from_Malaysia': random.randint(1, 6),
                'BC_from_Australia': random.randint(1, 6),
                'BC_from_Singapore': random.randint(1, 6),
                'BC_from_India': random.randint(1, 6),
                'BC_from_Hong_Kong': random.randint(1, 6)
            })

        if self.player.role() == 'B' or self.player.role() == 'C':
            answers.update({
                'A_from_China': random.randint(1, 6),
                'A_from_Malaysia': random.randint(1, 6),
                'A_from_Australia': random.randint(1, 6),
                'A_from_Singapore': random.randint(1, 6),
                'A_from_India': random.randint(1, 6),
                'A_from_Hong_Kong': random.randint(1, 6)
            })

        yield (pages.Main, answers)
