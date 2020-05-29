from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


class Constants(BaseConstants):
    name_in_url = 'values_task'
    players_per_group = None
    num_rounds = 1

    s_pairs = [
        ["You do not believe that homosexuality is a choice", "You believe that homosexuality is a choice"],
        ["You would tell a joke which insulted people who share your religious background.",
         "You would not tell a joke which insulted people who share your religious background."],
        ["You are proud to be a citizen of your home nation", "You are not proud to be a citizen of your home nation"],
    ]
    num_sp = len(s_pairs)
    exchange_amount = 50


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


def create_sp(op1, op2):
    return models.IntegerField(label="", choices=[[1, op1], [2, op2]], widget=widgets.RadioSelect)


class Player(BasePlayer):
    sp_count = models.IntegerField(initial=1)               # keeps track of page where option is displayed
    sp1 = create_sp(Constants.s_pairs[0][0], Constants.s_pairs[0][1])
    sp2 = create_sp(Constants.s_pairs[1][0], Constants.s_pairs[1][1])
    sp3 = create_sp(Constants.s_pairs[2][0], Constants.s_pairs[2][1])
    sp_accept_count = models.IntegerField(initial=1)        # keeps track of page where option to accept other statement is displayed
    sp1_accept = models.BooleanField(label="", widget=widgets.RadioSelect)
    sp2_accept = models.BooleanField(label="", widget=widgets.RadioSelect)
    sp3_accept = models.BooleanField(label="", widget=widgets.RadioSelect)
