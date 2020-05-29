from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Setup(WaitPage):
    wait_for_all_groups = True

    def after_all_players_arrive(self):
        # set the variables for the subsession and reset payoffs
        self.subsession.taking_player = 'A'
        if self.round_number == 1:
            self.subsession.deducting_player = 'B'
            for p in self.subsession.get_players():
                p.payoff = Constants.initial_payoffs[p.role()]
        elif self.round_number == 2 and self.session.config['stage2_active']:
            self.subsession.deducting_player = 'C'
        # set individual variables for players and set group structure
        groups = [[] for i in range(int(len(self.session.get_participants()) / Constants.players_per_group))]
        for p in self.subsession.get_players():
            p.br = p.participant.vars['birth_region']
            p.pi = p.participant.vars['pol_ideology']
            groups[p.participant.vars['group']].append(p)
        self.subsession.set_group_matrix(groups)


class Instructions(Page):

    def is_displayed(self):
        return self.round_number == 1


class Instructions2(Page):

    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return self.player.get_instruction_vars()


class Instructions3(Page):

    def is_displayed(self):
        return self.round_number == 1


class Instructions4(Page):

    def is_displayed(self):
        return self.round_number == 1


class Comprehension(Page):
    form_model = 'player'

    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return self.player.get_instruction_vars()

    def get_form_fields(self):
        if self.session.config['stage2_active']:
            return ['comp1', 'comp2', 'comp3']
        else:
            return ['comp1', 'comp3']

    def error_message(self, values):
        errs = []
        # question 1 errors
        if (not self.session.config['stage2_active'] and values['comp1'] != 1) or \
                (self.session.config['stage2_active'] and values['comp1'] != 2):
            errs.append('Question 1 is incorrect')
            self.player.comp1_wrong += 1
        # question 2/3 errors
        if self.session.config['stage2_active']:
            if self.session.config['stage2_active'] and values['comp2'] is not True:
                errs.append('Question 2 is incorrect')
                self.player.comp2_wrong += 1
            if values['comp3'] != 36:
                errs.append('Question 3 is incorrect')
                self.player.comp3_wrong += 1
        else:
            if values['comp3'] != 36:
                errs.append('Question 2 is incorrect')
                self.player.comp3_wrong += 1

        return errs


class Decision(Page):
    form_model = 'player'

    def is_displayed(self):
        return self.player.role() in [self.subsession.taking_player, self.subsession.deducting_player] and \
               not (self.round_number == 2 and not self.session.config['stage2_active'])

    def get_form_fields(self):
        if self.player.role() == self.subsession.taking_player:
            return ['chose_to_take']
        elif self.player.role() == self.subsession.deducting_player:
            return ['deduct_amount']

    def vars_for_template(self):
        return {
            'taking_player': self.subsession.taking_player,
            'deducting_player': self.subsession.deducting_player,
        }


class CalculatePayoffs(WaitPage):

    def is_displayed(self):
        return not (self.round_number == 2 and not self.session.config['stage2_active'])

    def after_all_players_arrive(self):
        self.group.set_payoffs()


class Feedback(Page):

    def is_displayed(self):
        return not (self.round_number == 2 and not self.session.config['stage2_active'])

    def vars_for_template(self):
        taking_player = self.group.get_player_by_role(self.subsession.taking_player)
        deduct_amount = self.group.get_player_by_role(self.subsession.deducting_player).deduct_amount
        payoffs_after_take = {p.role(): int(p.payoff_after_take) for p in self.group.get_players()}
        final_payoffs = {p.role(): int(p.participant.payoff) for p in self.group.get_players()}

        return {
            'points_were_taken': taking_player.chose_to_take,
            'taking_player': self.subsession.taking_player,
            'deducting_player': self.subsession.deducting_player,
            'payoffs_after_take': dict(sorted(payoffs_after_take.items())),
            'deduct_amount': int(deduct_amount),
            'multiplied_deduct_amount': int(Constants.deduct['multiplier']*deduct_amount),
            'final_payoffs': dict(sorted(final_payoffs.items()))
        }


page_sequence = [
    Setup,
    Instructions,
    Instructions2,
    Instructions3,
    Instructions4,
    Comprehension,
    Decision,
    CalculatePayoffs,
    Feedback
]
