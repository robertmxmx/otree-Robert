from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
import time, random


class PlayerBot(Bot):

    def play_round(self):
        if self.round_number == 1:
            yield (pages.Instructions)

            if 1 <= self.player.id_in_group <= 4:
                yield (pages.Main, {'user_text': self.player.correct_text})
            else:
                yield (pages.Main, {'user_text': 0})

            time.sleep(self.session.config['ret_time'])
            yield (pages.Main, {'user_text': 0})

        if self.round_number == Constants.num_rounds:
            yield (pages.Results)

            if 1 <= self.player.id_in_group <= int(len(self.group.get_players()) / 2):
                yield (pages.ChooseStartColor, {'start_color': random.choice(['red', 'blue'])})
