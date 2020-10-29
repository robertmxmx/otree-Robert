from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
import random
from otree.api import Submission

from _myshared import uploader

class PlayerBot(Bot):

    def play_round(self):
        if self.participant.id_in_session == 2:
            yield (pages.PayID, { 'pay_id': 'p1' })
            yield Submission(pages.InvalidPayID, check_html=False)
        else:
            yield (pages.PayID, {
                'pay_id': uploader.USERDATA[self.participant.id_in_session-1]['pay_id']
            })

    #     yield (pages.Main, {
    #         'birth_region': 4 if self.participant.id_in_session % 3 == 0 else 1,
    #         'other_br': 'some region',
    #         'pi_q1': random.randint(1, 7),
    #         'pi_q2': random.randint(1, 7),
    #         'pi_q3': random.randint(1, 7),
    #         'pi_q4': random.randint(1, 7),
    #         'pi_q5': random.randint(1, 7),
    #         'pi_q6': random.randint(1, 7),
    #         'pi_q7': random.randint(1, 7),
    #     })
