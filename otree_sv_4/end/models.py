from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)
import random
import constants

class Constants(BaseConstants):
    name_in_url = 'end'
    players_per_group = None
    num_rounds = 1

    opt_out_text = constants.opt_out_text


class Subsession(BaseSubsession):
    paid_task = models.IntegerField()
    chosen_statement = models.StringField()
    switch_price = models.IntegerField()

    def creating_session(self):
        self.paid_task = random.randint(1, 3)

        self.chosen_statement = random.choice(list(constants.statements.keys()))
        self.switch_price = random.randint(constants.min_bid, constants.max_bid)


class Group(BaseGroup):
    def set_payoffs(self):
        for player in self.get_players():
            paid_task = self.subsession.paid_task

            if paid_task == 1 or paid_task == 3:
                variables = player.participant.vars['task%d_vars' % paid_task]
                player.participant.payoff = variables['final_payoff']
            else:
                statement_bids = player.participant.vars['statements_bid']
                bid = statement_bids[self.subsession.chosen_statement]

                if bid == Constants.opt_out_text:
                    player.participant.payoff = 0
                else:
                    bid = int(bid)
                    if self.subsession.switch_price < bid:
                        player.participant.payoff = 0
                    else:
                        player.participant.payoff = self.subsession.switch_price


class Player(BasePlayer):
    pass
