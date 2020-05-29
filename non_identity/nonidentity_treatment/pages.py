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
    form_fields = [
        't1_c1_1', 't1_c1_2', 't1_c1_3',
        't1_c2_1', 't1_c2_2', 't1_c2_3',
        't1_c3'
    ]

    def error_message(self, values):
        error_list = []

        if values['t1_c1_1'] != 12 or values['t1_c1_2'] != 0 or values['t1_c1_3'] != 2:
            self.player.t1_c1_wrong += 1
            error_list.append("Question 1 is incorrect")

        if values['t1_c2_1'] != 10 or values['t1_c2_2'] != 10 or values['t1_c2_3'] != 0:
            self.player.t1_c2_wrong += 1
            error_list.append("Question 2 is incorrect")

        if values['t1_c3'] != 2:
            self.player.t1_c3_wrong += 1
            error_list.append("Question 3 is incorrect")

        return error_list


class Task1(Page):
    form_model = 'player'
    form_fields = ['t1_option']

    def before_next_page(self):
        self.player.t1_payoff, self.player.t1_participantA_payoff, self.player.t1_participantB_payoff \
            = self.player.set_op_payoff(True, 0, self.player.t1_option)


class Task2aInstructions(Page):
    pass


class Task2aComprehension(Page):
    form_model = 'player'
    form_fields = ['t2a_c1', 't2a_c2', 't2a_c3']

    def error_message(self, values):
        error_list = []

        if values['t2a_c1'] != 2:
            self.player.t2a_c1_wrong += 1
            error_list.append("Question 1 is incorrect")

        if values['t2a_c2'] != 3:
            self.player.t2a_c2_wrong += 1
            error_list.append("Question 2 is incorrect")

        if values['t2a_c3'] != 1:
            self.player.t2a_c3_wrong += 1
            error_list.append("Question 3 is incorrect")

        return error_list


class Task2a(Page):
    form_model = 'player'
    form_fields = ['t2a_option']

    def before_next_page(self):
        if self.player.t2a_option != 3:
            self.player.t2a_payoff, self.player.t2a_partner_payoff \
                = self.player.set_op_payoff(False, self.player.t2a_version, self.player.t2a_option)


class Task2aRevealed(Page):
    form_model = 'player'

    def is_displayed(self):
        return self.player.t2a_option == 3

    def get_form_fields(self):
        if self.player.t2a_option == 3:
            return ['t2a_revealed_option']

    def vars_for_template(self):
        return {
            't2a_version': self.player.t2a_version
        }

    def before_next_page(self):
            self.player.t2a_payoff, self.player.t2a_partner_payoff \
                = self.player.set_op_payoff(False, self.player.t2a_version, self.player.t2a_revealed_option)


class Task2bInstructions(Page):
    pass


class Task2bComprehension(Page):
    form_model = 'player'
    form_fields = ['t2b_c1_1', 't2b_c1_2', 't2b_c2_1', 't2b_c2_2']

    def error_message(self, values):
        error_list = []

        if values['t2b_c1_1'] != 12 or values['t2b_c1_2'] != 2:
            self.player.t2b_c1_wrong += 1
            error_list.append("Question 1 is incorrect")

        if values['t2b_c2_1'] != 10 or values['t2b_c2_2'] != 10:
            self.player.t2b_c2_wrong += 1
            error_list.append("Question 2 is incorrect")

        return error_list


class Task2b(Page):
    form_model = 'player'
    form_fields = ['t2b_option']

    def before_next_page(self):
            self.player.t2b_payoff, self.player.t2b_partner_payoff \
                = self.player.set_op_payoff(False, 1, self.player.t2b_option)


class Task2cInstructions(Page):
    pass


class Task2cComprehension(Page):
    form_model = 'player'
    form_fields = ['t2c_c1_1', 't2c_c1_2', 't2c_c2_1', 't2c_c2_2']

    def error_message(self, values):
        error_list = []

        if values['t2c_c1_1'] != 12 or values['t2c_c1_2'] != 10:
            self.player.t2c_c1_wrong += 1
            error_list.append("Question 1 is incorrect")

        if values['t2c_c2_1'] != 10 or values['t2c_c2_2'] != 2:
            self.player.t2c_c2_wrong += 1
            error_list.append("Question 2 is incorrect")

        return error_list


class Task2c(Page):
    form_model = 'player'
    form_fields = ['t2c_option']

    def before_next_page(self):
        self.player.t2c_payoff, self.player.t2c_partner_payoff \
            = self.player.set_op_payoff(False, 2, self.player.t2c_option)
        self.player.set_payoff()


page_sequence = [
    AllWait,

    Task1Instructions,
    Task1Comprehension,
    Task1,

    AllWait,

    Task2aInstructions,
    Task2aComprehension,
    Task2a,
    Task2aRevealed,

    AllWait,

    Task2bInstructions,
    Task2bComprehension,
    Task2b,

    AllWait,

    Task2cInstructions,
    Task2cComprehension,
    Task2c,
]
