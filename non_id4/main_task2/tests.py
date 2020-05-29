from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
from otree.api import Submission, SubmissionMustFail
import random


class PlayerBot(Bot):

    def play_round(self):
        a_revealed = random.choice([True, False])
        a_option = random.choice([1, 2])
        b_option = random.choice([1, 2])
        c_option = random.choice([1, 2])

        yield (pages.AInstructions)
        yield SubmissionMustFail(pages.AComprehension, {"a_comp1": 1, "a_comp2": 2, "a_comp3": 2})
        yield (pages.AComprehension, Constants.a_comp_answers)
        if a_revealed:
            yield (pages.AChoice, {'a_revealed': a_revealed})
            yield Submission(pages.ARevealed, {'a_option': a_option})
        else:
            yield (pages.AChoice, {'a_option': a_option})

        yield (pages.BInstructions)
        yield SubmissionMustFail(pages.BComprehension, {"b_comp1a": 5, "b_comp1b": 3, "b_comp2a": 2, "b_comp2b": 1})
        yield (pages.BComprehension, Constants.b_comp_answers)
        yield (pages.BChoice, {'b_option': b_option})

        yield (pages.CInstructions)
        yield SubmissionMustFail(pages.CComprehension, {"c_comp1a": 2, "c_comp1b": 7, "c_comp2a": 1, "c_comp2b": 7})
        yield (pages.CComprehension, Constants.c_comp_answers)
        yield (pages.CChoice, {'c_option': c_option})
