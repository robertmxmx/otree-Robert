from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
import random
from otree.api import Submission

from _myshared import uploader

class PlayerBot(Bot):

    def play_round(self):
        yield (pages.InitialSurvey, {
            'birth_region': 3,
            'pi_q1': 1,
            'pi_q2': 1,
            'pi_q3': 1,
            'pi_q4': 1,
            'pi_q5': 1,
            'pi_q6': 1,
            'pi_q7': 1
        })