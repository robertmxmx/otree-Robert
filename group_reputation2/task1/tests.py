from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
import random


class PlayerBot(Bot):

    def play_round(self):
        yield (pages.Main, {
            'birth_region': 1 if self.participant.id_in_session == 3 else 2,
            'other_br': 'some region',
            'pi_q1': random.randint(1, 7),
            'pi_q2': random.randint(1, 7),
            'pi_q3': random.randint(1, 7),
            'pi_q4': random.randint(1, 7),
            'pi_q5': random.randint(1, 7),
            'pi_q6': random.randint(1, 7),
            'pi_q7': random.randint(1, 7),
        })
