from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Instructions(Page):

    def is_displayed(self):
        return self.round_number == 1


class DetailedInstructions(Page):

    def is_displayed(self):
        return self.round_number == 1


class WaitInitial(WaitPage):

    def after_all_players_arrive(self):
        self.group.get_town_color()


class MoveDecision(Page):
    form_model = 'player'
    form_fields = ['chose_to_switch']

    def get_timeout_seconds(self):
        if self.round_number <= 6:
            return 2*60
        else:
            return 30

    def chose_to_switch_choices(self):
        if self.player.town == 'red':
            return [[True, 'Move to Blue Town'], [False, 'Stay in Red Town']]
        else:
            return [[True, 'Move to Red Town'], [False, 'Stay in Blue Town']]

    def vars_for_template(self):
        return self.group.get_common_data()

    def before_next_page(self):
        if self.timeout_happened:
            self.player.move_timeout_action()


class WaitMove(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_town_after_move()
        self.group.set_payoff_after_move()


class PayoffAfterMoving(Page):
    timeout_seconds = 30

    def vars_for_template(self):
        return_dict = {}
        return_dict.update(self.group.get_common_data())

        if self.round_number > 1:
            return_dict['move_choice'] = 'move to' if self.player.in_round(self.round_number-1).town != self.player.town else 'stay in'

        return return_dict


class End(WaitPage):

    def after_all_players_arrive(self):
        for p in self.group.get_players():
            p.finalize()


page_sequence = [
    Instructions,
    DetailedInstructions,

    WaitInitial,

    MoveDecision,
    WaitMove,
    PayoffAfterMoving,

    End,
]
