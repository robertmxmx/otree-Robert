from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import time

"""
A portion of the following code has been used from:
Title:          otree_rets Source Code
Author:         Kephart, C
Date:           2017
Available at:   https://github.com/EconomiCurtis/otree_rets
"""


class Instructions(Page):

    def is_displayed(self):
        return self.round_number == 1

    def before_next_page(self):
        # user has ret_timer seconds to complete as many pages as possible
        self.participant.vars['expiry_timestamp'] = time.time() + self.session.config['ret_time']
        self.participant.payoff = c(0)


class Main(Page):
    form_model = 'player'
    form_fields = ['user_text']

    def get_timeout_seconds(self):
        return self.participant.vars['expiry_timestamp'] - time.time()

    def is_displayed(self):
        return self.participant.vars['expiry_timestamp'] - time.time() > 0

    def vars_for_template(self):
        return {
            'total_payoff': round(self.player.participant.payoff),
        }

    def before_next_page(self):
        self.player.score_round()


class Results(Page):

    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):

        table_rows = []
        for prev_player in self.player.in_all_rounds():
            if prev_player.user_text is not None:
                row = {
                    'round_number': prev_player.round_number,
                    'correct_text': prev_player.correct_text,
                    'user_text': prev_player.user_text,
                    'is_correct': prev_player.is_correct,
                }
                table_rows.append(row)

        return {
            'table_rows': table_rows,
            'total_payoff': round(self.player.participant.payoff),
        }


class FindTop(WaitPage):

    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def after_all_players_arrive(self):
        scores = [
            {
                'id': p.id_in_group,
                'score': round(p.participant.payoff)
            } for p in self.group.get_players()
        ]

        sorted_scores = sorted(scores, key=lambda k: k['score'], reverse=True)
        top_scorers = [sorted_scores[i]['id'] for i in range(0, int(len(self.group.get_players()) / 2))]

        for p in self.group.get_players():
            if p.id_in_group in top_scorers:
                p.top_scorer = True
            else:
                p.top_scorer = False


class ChooseStartColor(Page):
    form_model = 'player'
    form_fields = ['start_color']

    def is_displayed(self):
        return self.round_number == Constants.num_rounds and self.player.top_scorer


class AssignTowns(WaitPage):

    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def after_all_players_arrive(self):
        self.group.assign_players()


page_sequence = [
    Instructions,
    Main,
    Results,
    FindTop,
    ChooseStartColor,
    AssignTowns,
]
