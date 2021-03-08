from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

from _myshared.constants import REGIONS

class Constants(BaseConstants):
    name_in_url = 'task2'
    players_per_group = 3
    num_rounds = 2

    initial_payoffs = {'A': 20, 'B': 110, 'C': 110}
    take_amount = 100
    deduct = {'min': 0, 'max': 10, 'multiplier': 12}
    additional_amount = 10


class Subsession(BaseSubsession):
    taking_player = models.StringField()
    deducting_player = models.StringField()

    def group_by_arrival_time_method(self, waiting_players):
        group_num = waiting_players[0].participant.vars['group']
        potential_group = [p for p in waiting_players if p.participant.vars['group'] == group_num]

        if len(potential_group) == Constants.players_per_group:
            return potential_group

    def creating_session(self):
        # set player role for the round
        self.taking_player = 'A'
        self.deducting_player = 'B' if self.round_number == 1 else 'C'

        if self.round_number != 1:
            self.group_like_round(1)


class Group(BaseGroup):

    def init_round(self):
        for p in self.get_players():
            p.participant.payoff = 0
            p.payoff = Constants.initial_payoffs[p.role()]
            p.br = p.participant.vars['birth_region']
            p.pi = p.participant.vars['pol_ideology']


    def set_payoffs(self):
        taking_player = self.get_player_by_role(self.subsession.taking_player)
        deducting_player = self.get_player_by_role(self.subsession.deducting_player)
        other_player = None

        for p in self.get_players():
            if p not in [taking_player, deducting_player]:
                other_player = p

        # set if ECU was taken
        if taking_player.chose_to_take:
            deducting_player.payoff -= Constants.take_amount
            taking_player.payoff += Constants.take_amount

        # set all players payoff after the choice of whether to take
        for p in self.get_players():
            p.payoff_after_take = p.participant.payoff

        # set deduction amount
        if taking_player.chose_to_take:
            deducting_player.payoff -= deducting_player.deduct_amount
            taking_player.payoff -= Constants.deduct['multiplier']*deducting_player.deduct_amount

        # Set payoffs for B/C guess
        if self.round_number == 1:
            if other_player.will_spend == deducting_player.deduct_amount:
                other_player.payoff += Constants.additional_amount
                other_player.participant.vars['bonus'] = Constants.additional_amount
            else:
                other_player.participant.vars['bonus'] = 0
        else:
            previous_other_player = deducting_player.in_round(self.round_number - 1)
            bonus_multiplier = 0
            
            if other_player.will_spend_guess == previous_other_player.will_spend:
                bonus_multiplier += 1

            if other_player.should_spend_guess == previous_other_player.should_spend:
                bonus_multiplier += 1
                
            other_player.payoff += bonus_multiplier * Constants.additional_amount
            other_player.participant.vars['bonus'] = bonus_multiplier * Constants.additional_amount


class Player(BasePlayer):
    br = models.IntegerField()
    pi = models.IntegerField()
    comp1 = models.IntegerField(
        label='In Task 1, who will A have the opportunity to take ECU from?',
        choices=[[1, 'B'], [2, 'C'], [3, 'both B and C']],
        widget=widgets.RadioSelect
    )
    comp2 = models.BooleanField(
        label='In Task 2, will A have the opportunity to take ECU from C?',
        widget=widgets.RadioSelectHorizontal,
        choices=[[True, 'True'], [False, 'False']]
    )
    comp3 = models.BooleanField(
        label='In Task 2, before making a decision, will A learn how B reacted to A’s decision in Task 1?',
        widget=widgets.RadioSelectHorizontal,
        choices=[[True, 'True'], [False, 'False']]
    )
    comp4 = models.IntegerField(
        label='When will C learn about the membership of the group?',
        choices=[[1, 'at the end of task 1'], [2, 'at the end of task 2'], [3, 'never']],
        widget=widgets.RadioSelect
    )
    comp5 = models.IntegerField(
        label='''If, after A takes ECU from B, Participant B chooses to spend 3 ECU to reduce A’s endowment, 
            how many ECU will A lose?''',
        min=0
    )
    comp1_wrong = models.IntegerField(initial=0)
    comp2_wrong = models.IntegerField(initial=0)
    comp3_wrong = models.IntegerField(initial=0)
    comp4_wrong = models.IntegerField(initial=0)
    comp5_wrong = models.IntegerField(initial=0)
    chose_to_take = models.BooleanField()
    payoff_after_take = models.CurrencyField()
    deduct_amount = models.CurrencyField(initial=0, min=Constants.deduct['min'], max=Constants.deduct['max'])

    will_spend = models.CurrencyField(min=Constants.deduct['min'], max=Constants.deduct['max'])
    should_spend = models.CurrencyField(min=Constants.deduct['min'], max=Constants.deduct['max'])

    will_spend_guess = models.CurrencyField(min=Constants.deduct['min'], max=Constants.deduct['max'])
    should_spend_guess = models.CurrencyField(min=Constants.deduct['min'], max=Constants.deduct['max'])

    def role(self):
        return self.participant.vars['role']

    def get_instruction_vars(self):
        # returns variables that are used on the instruction screen
        sorted_by = self.participant.vars['sorted_by']
        deducting_player = self.group.get_player_by_role(self.subsession.deducting_player)
        return_dict = {'sorted_by': sorted_by}

        if sorted_by:
            return_dict.update({
                'other_knowledge_player': self.subsession.deducting_player if self.role() == self.subsession.taking_player else self.subsession.taking_player
            })
            if sorted_by == 'birth_region':
                return_dict.update({'same_region': REGIONS[deducting_player.br-1]})
            elif sorted_by == 'pol_ideology':
                return_dict.update({'same_ideology': 'progressive' if deducting_player.pi == 1 else 'conservative'})

        return return_dict
