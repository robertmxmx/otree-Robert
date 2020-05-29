from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random


class Constants(BaseConstants):
    name_in_url = 'end'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    def creating_session(self):
        ran_nums = random.sample(range(1, 5+1), 2)
        # self.session.vars['payoff_tasks'] = [ran_nums[0], ran_nums[1]]
        for g in self.get_groups():
            g.chosen1 = ran_nums[0]
            g.chosen2 = ran_nums[1]


class Group(BaseGroup):
    chosen1 = models.IntegerField()
    chosen2 = models.IntegerField()


class Player(BasePlayer):
    t1_payoff = models.CurrencyField()
    t2_payoff = models.CurrencyField()
    t3_payoff = models.CurrencyField()
    t4_payoff = models.CurrencyField()
    t5_payoff = models.CurrencyField()
    total = models.CurrencyField()
    total_no3 = models.CurrencyField()
