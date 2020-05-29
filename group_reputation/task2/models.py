from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import shared


class Constants(BaseConstants):
    name_in_url = 'task2'
    players_per_group = 3
    num_rounds = 2

    initial_payoffs = {'A': 20, 'B': 110, 'C': 110}
    take_amount = 100
    deduct = {'min': 0, 'max': 10, 'multiplier': 12}


class Subsession(BaseSubsession):
    taking_player = models.StringField()
    deducting_player = models.StringField()


class Group(BaseGroup):

    def set_payoffs(self):
        taking_player = self.get_player_by_role(self.subsession.taking_player)
        deducting_player = self.get_player_by_role(self.subsession.deducting_player)

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


class Player(BasePlayer):
    br = models.IntegerField()
    pi = models.IntegerField()
    comp1 = models.IntegerField(label='How many times will A have the opportunity to take ECU?')
    comp2 = models.BooleanField(label='''In stage 2, A will have the opportunity to take ECU from C. Will C know 
        what happened in stage 1?''', widget=widgets.RadioSelectHorizontal)
    comp3 = models.IntegerField(label='''If Participant B chooses to spend 3 ECU to reduce A's endowment, how many 
        ECU will A lose?''')
    comp1_wrong = models.IntegerField(initial=0)
    comp2_wrong = models.IntegerField(initial=0)
    comp3_wrong = models.IntegerField(initial=0)
    chose_to_take = models.BooleanField()
    payoff_after_take = models.CurrencyField()
    deduct_amount = models.CurrencyField(min=Constants.deduct['min'], max=Constants.deduct['max'])

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
                return_dict.update({'same_region': shared.regions[deducting_player.br-1]})
            elif sorted_by == 'pol_ideology':
                return_dict.update({'same_ideology': 'left' if deducting_player.pi == 1 else 'right'})

        return return_dict
