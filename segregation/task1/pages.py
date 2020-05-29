from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class WaitInitial(WaitPage):

    def after_all_players_arrive(self):
        self.group.get_town_color()


class Confirm(Page):

    def is_displayed(self):
        return self.group.at_starting_periods()

    def vars_for_template(self):
        return self.group.get_common_data()


class MoveDecision(Page):
    form_model = 'player'
    form_fields = ['chose_to_switch']

    def get_timeout_seconds(self):
        if self.round_number <= 6:
            return 2*60
        else:
            return 30

    def is_displayed(self):
        return not self.group.at_starting_periods()

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

        if not self.group.at_starting_periods():
            return_dict['move_choice'] = 'move to' if self.player.in_round(self.round_number-1).town != self.player.town else 'stay in'

        return return_dict

    def before_next_page(self):
        self.player.create_town_pop_deduction_fields()


class DeductionDecision(Page):
    form_model = 'player'

    def is_displayed(self):
        return self.group.at_deduction_round()

    def get_timeout_seconds(self):
        if len(self.participant.vars['town_pop']) == 0:
            return None
        else:
            if self.round_number <= 6:
                return 2 * 60
            else:
                return 30

    def get_form_fields(self):
        return self.participant.vars['deduction_fields']

    def vars_for_template(self):
        return dict(self.group.get_common_data(), **{
            'deduction_fields': self.participant.vars['deduction_fields'],
            'town_pop': self.participant.vars['town_pop'],
            'empty_town': True if len(self.participant.vars['town_pop']) == 0 else False
        })

    def before_next_page(self):
        if self.timeout_happened:
            self.player.deduct_timeout_action()


class WaitDeduct(WaitPage):

    def is_displayed(self):
        return self.group.at_deduction_round()

    def after_all_players_arrive(self):
        self.group.set_payoff_after_deduct()


class Summary(Page):
    timeout_seconds = 30

    def is_displayed(self):
        return self.group.at_deduction_round()

    def vars_for_template(self):
        return self.group.get_common_data()


class End(WaitPage):

    def after_all_players_arrive(self):
        for p in self.group.get_players():
            p.finalize()


page_sequence = [
    WaitInitial,

    Confirm,

    MoveDecision,
    WaitMove,
    PayoffAfterMoving,
    DeductionDecision,
    WaitDeduct,
    Summary,

    End,
]
