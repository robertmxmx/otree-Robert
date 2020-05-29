from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class AssignID(WaitPage):

    def after_all_players_arrive(self):
        self.group.initialise_game()


class Beginning(Page):

    def vars_for_template(self):
        return {
            'round_number': self.round_number,
            'total_rounds': Constants.num_rounds,
            'player_id': self.player.player_id
        }


class Stage1Decision(Page):
    form_model = 'group'
    form_fields = ['r_pressed']

    def is_displayed(self):
        return self.round_number != Constants.sp_round_num and \
               self.player.player_id == self.group.r_presser


class WaitForRed(WaitPage):

    def is_displayed(self):
        return self.round_number != Constants.sp_round_num


class Stage2Decision(Page):
    form_model = 'group'

    def is_displayed(self):
        return self.round_number != Constants.sp_round_num and \
                self.group.r_pressed and \
               (self.player.player_id == self.group.g1_presser or self.player.player_id == self.group.g2_presser)

    def get_form_fields(self):
        if self.player.player_id == self.group.g1_presser:
            return ['g1_pressed']
        else:
            return ['g2_pressed']

    def vars_for_template(self):
        return {
            'r_presser': self.group.r_presser,
            'g_presser': 1 if self.player.player_id == self.group.g1_presser else 2
        }


class SetButtonPayoffs(WaitPage):

    def is_displayed(self):
        return self.round_number != Constants.sp_round_num

    def after_all_players_arrive(self):
        self.group.set_button_payoffs()


class Stage2Feedback(Page):

    def is_displayed(self):
        return self.round_number != Constants.sp_round_num

    def vars_for_template(self):
        return_dict = {
            'r_presser': self.group.r_presser,
            'r_pressed': self.group.r_pressed,
            'r_affected': self.group.r_affected,
            'stage1_earnings': float(self.player.stage1_earnings),
        }

        if self.group.r_pressed:
            self.group.set_green_pressers_decliners()
            return_dict.update({
                'g1_presser': self.group.g1_presser,
                'g2_presser': self.group.g2_presser,
                'green_pressers': self.group.g_pressers,
                'green_decliners': self.group.g_decliners,
                'stage2_earnings': float(self.player.stage2_earnings)
            })

        return return_dict


class Stage3Decision(Page):
    form_model = 'group'
    form_fields = ['r_deduction_pts', 'g_deduction_pts']

    def is_displayed(self):
        return self.round_number != Constants.sp_round_num and \
               self.group.r_pressed and \
               self.player.player_id == self.group.unaffected

    def error_message(self, values):
        err_arr = []

        if values['r_deduction_pts'] + values['g_deduction_pts'] > 30:
            err_arr.append("Total deduction points must be less than or equal to 30")

        if self.group.g1_pressed and self.group.g2_pressed and values['g_deduction_pts'] != 0:
            err_arr.append("Zero points must be assigned to green button non-presser as green button was pressed")

        return err_arr


class WaitForDeduction(WaitPage):

    def is_displayed(self):
        return self.round_number != Constants.sp_round_num and \
               self.group.r_pressed


class Stage3Agreement(Page):
    form_model = 'group'
    form_fields = ['deduction_accepted']

    def is_displayed(self):
        return self.round_number != Constants.sp_round_num and \
               self.group.r_pressed and \
               self.player.player_id == self.group.r_affected

    def vars_for_template(self):
        x = float(self.group.r_deduction_pts)
        y = float(self.group.g_deduction_pts)
        if self.group.g1_pressed or self.group.g2_pressed:
            n = 0
        else:
            n = 2
        return {
            'r_deduction_pts': x,
            'g_deduction_pts': y,
            'cost_to_deductor': (x + (n*y))/2,
            'r_deduction_pts_x3': 3*x,
            'g_deduction_pts_x3': 3*y,
        }


class SetDeductionPoints(WaitPage):

    def is_displayed(self):
        return self.round_number != Constants.sp_round_num and \
               self.group.r_pressed

    def after_all_players_arrive(self):
        if self.group.deduction_accepted:
            self.group.set_deduction_points()


class SpecialRound(Page):
    form_model = 'player'
    form_fields = ['r_pressed', 'g_pressed', 'd_un_r0g', 'd_un_r1g', 'd_un_r2g', 'd_aff_r0g', 'd_aff_r1g', 'd_aff_r2g']

    def is_displayed(self):
        return self.round_number == Constants.sp_round_num


class SetSpecialPayoff(WaitPage):

    def is_displayed(self):
        return self.round_number == Constants.sp_round_num

    def after_all_players_arrive(self):
        self.group.set_special_payoff()


class Feedback(Page):

    def is_displayed(self):
        return self.group.r_pressed

    def vars_for_template(self):

        return {
            'r_presser': self.group.r_presser,
            'r_pressed': self.group.r_pressed,
            'r_affected': self.group.r_affected,
            'stage1_earnings': float(self.player.stage1_earnings),
            'g1_presser': self.group.g1_presser,
            'g2_presser': self.group.g2_presser,
            'green_decliners': self.group.g_decliners,
            'green_pressers': self.group.g_pressers,
            'stage2_earnings': float(self.player.stage2_earnings),
            'r_deduction_pts': float(self.group.r_deduction_pts),
            'g_deduction_pts': float(self.group.g_deduction_pts),
            'payoff': float(self.player.payoff),
            'deduction_accepted': self.group.deduction_accepted
        }


class StorePayoff(WaitPage):

    def after_all_players_arrive(self):
        for p in self.group.get_players():
            p.participant.vars['payoffs'].append(p.payoff)
            p.payoff = 0


page_sequence = [
    AssignID,
    Beginning,

    Stage1Decision,
    WaitForRed,

    Stage2Decision,
    SetButtonPayoffs,
    Stage2Feedback,

    Stage3Decision,
    WaitForDeduction,
    Stage3Agreement,
    SetDeductionPoints,

    SpecialRound,
    SetSpecialPayoff,
    Feedback,

    StorePayoff
]