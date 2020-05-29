from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import random


class Instructions(Page):

    def vars_for_template(self):
        return {'participant_is_a': True if self.participant.id_in_session % 2 else False}


class Comprehension(Page):
    form_model = 'player'
    form_fields = ['c1', 'c2']

    def error_message(self, values):
        errs = []

        if values['c1'] != False:
            self.player.c1_wrong += 1
            errs.append("Question 1 is incorrect")

        if values['c2'] != 1:
            self.player.c2_wrong += 1
            errs.append("Question 2 is incorrect")

        return errs

    def vars_for_template(self):
        return {'participant_is_a': True if self.participant.id_in_session % 2 else False}


class Wait(Page):
    pass


class ConcealmentRequests(Page):
    timeout_seconds = 3*60 + 30
    timeout_submission = {k: 0 for k in ['conceal'+str(i) for i in range(1, Constants.s_total+1)]}
    form_model = 'player'
    form_fields = ['conceal'+str(i) for i in range(1, Constants.s_total+1)]

    def is_displayed(self):
        return not self.participant.id_in_session % 2

    def vars_for_template(self):
        s_subset = []
        sp_data = self.participant.vars['sp_data'].copy()

        # format correctly
        for i in Constants.statement_list:
            statement = sp_data[i]['original_statement']
            price = sp_data[i]['bid_amount']

            if price == "out":
                item = statement + " (" + str(price) + ")"
            else:
                item = statement + " ($" + str(price) + ")"

            s_subset.append({'item': item, 'index': i})     # todo: change this to 'index': i+1

        random.shuffle(s_subset)
        self.participant.vars['s_subset'] = s_subset.copy()

        return {'s_subset': self.participant.vars['s_subset']}

    def error_message(self, values):
        sorted_input = [x for x in values.values() if x is not None]
        if sorted(sorted_input) != [i for i in range(1, len(sorted_input)+1)]:
            return 'invalid input'


class ProcessingPage(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_random_conceal()
        for p in self.group.get_players():
            if not p.participant.id_in_session % 2:
                p.set_revealed()


class ConcealmentOutcome(Page):

    def is_displayed(self):
        return not self.participant.id_in_session % 2

    def vars_for_template(self):
        return {
            'num_random_conceal': self.group.num_random_conceal,
            'num_to_reveal': Constants.s_total - self.group.num_random_conceal,
            'num_chosen': self.player.num_chosen,
            'num_to_conceal': min(self.player.num_chosen, self.group.num_random_conceal)
        }


class Revelation(Page):

    def vars_for_template(self):
        if self.participant.id_in_session % 2:
            player_statements = self.player.get_others_in_group()[0].participant.vars['s_revealed']
        else:
            player_statements = self.participant.vars['s_revealed']
        return {
            'participant_is_a': True if self.participant.id_in_session % 2 else False,
            'num_player': len(player_statements),
            'player_statements': player_statements
        }


page_sequence = [
    Instructions,
    Comprehension,
    Wait,
    ConcealmentRequests,
    ProcessingPage,
    ConcealmentOutcome,
    Revelation
]
