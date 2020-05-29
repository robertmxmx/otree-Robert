from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import random


class AllWait(WaitPage):
    wait_for_all_groups = True


class Task1Instructions(Page):
    pass


class Task1Comprehension(Page):
    form_model = 'player'
    form_fields = ['t1_c1_1', 't1_c1_2', 't1_c2_1', 't1_c2_2']

    def error_message(self, values):
        error_list = []

        if values['t1_c1_1'] != 10 or values['t1_c1_2'] != 10:
            self.player.t1_c1_wrong += 1
            error_list.append("Question 1 is incorrect")

        if values['t1_c2_1'] != 12 or values['t1_c2_2'] != 2:
            self.player.t1_c2_wrong += 1
            error_list.append("Question 2 is incorrect")

        return error_list


class Task1(Page):
    form_model = 'player'
    form_fields = ['t1_option']

    def before_next_page(self):
        self.player.set_payoff()


page_sequence = [
    AllWait,

    Task1Instructions,
    Task1Comprehension,
    Task1,
]