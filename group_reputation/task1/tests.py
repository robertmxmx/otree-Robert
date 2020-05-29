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
            'pi_q1': 1 if self.participant.id_in_session in [4, 5] else 7,
            'pi_q2': 1 if self.participant.id_in_session in [4, 5] else 7,
            'pi_q3': 1 if self.participant.id_in_session in [4, 5] else 7,
            'pi_q4': 1 if self.participant.id_in_session in [4, 5] else 7,
            'pi_q5': 1 if self.participant.id_in_session in [4, 5] else 7,
            'pi_q6': 1 if self.participant.id_in_session in [4, 5] else 7,
            'pi_q7': 1 if self.participant.id_in_session in [4, 5] else 7,
        })
