from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
import random


class PlayerBot(Bot):

    def play_round(self):
        yield (pages.Main, {
            'q1': random.choice([
                'Male',
                'Female',
                'Other',
                'Prefer not to say'
            ]),
            'q2': random.choice([
                'Nothing',
                'Law',
                'Political Science',
                'Economics',
                'Accounting',
                'Marketing',
                'Mathematics',
                'Computer Science',
                'Psychology',
                'Medicine',
                'Natural Sciences',
                'Languages',
                'Philosophy',
                'Other'
            ]),
            'q3': 'Antarctica',
            'q4': random.randint(0, 100),
            'q5': random.choice([
                'Christianity',
                'Judaism',
                'Islam',
                'Hinduism',
                'Buddhism',
                'Sikhism',
                'Atheism/Agnosticism/Secularism',
                'Other'
            ]),
            'q6': random.choice([
                '0',
                '1-2',
                '3-6',
                '7-12',
                'more than 12'
            ]),
        })
