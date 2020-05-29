from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
from otree.api import Submission
import random

class PlayerBot(Bot):
    def play_round(self):
        yield Submission(pages.Instructions, check_html=False)
        
        yield pages.Revelation
        
        if self.player.role() == 'A':
            yield (pages.ADecision, dict(
                points_taken=random.choice([True, False]))
            )
        elif self.player.role() == 'B':
            yield (pages.BDecision, dict(
                points_retaliated=random.randint(
                    Constants.deduction['min'], 
                    Constants.deduction['max']
                )
            ))

        yield pages.Outcome   
        
        if self.player.role() == 'A':
            yield (pages.Survey, dict(surveyq_part_A=1, surveyq_why='idk'))
        elif self.player.role() == 'B':
            yield (pages.Survey, dict(surveyq_part_B=1, surveyq_why='idk'))
