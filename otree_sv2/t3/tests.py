from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
import random
from otree.api import Submission


class PlayerBot(Bot):

    def play_round(self):
        num_conceal = random.randint(1, Constants.s_total)      # pick a random number of statements to rank
        temp_arr = [i for i in range(1, num_conceal + 1)]
        random.shuffle(temp_arr)

        yield Submission(pages.Instructions, check_html=False)
        yield (pages.Comprehension, {
            'c1': False,
            'c2': 1
        })
        yield Submission(pages.Wait, check_html=False)

        if not self.participant.id_in_session % 2:
            yield (pages.ConcealmentRequests, {
                'conceal'+str(i): temp_arr[i-1] for i in range(1, num_conceal + 1)
            })

            # yield (pages.ConcealmentRequests, {
            #     'conceal1': 1, 'conceal2': 2, 'conceal3': 3
            # })

            yield (pages.ConcealmentOutcome)

        yield (pages.Revelation)
