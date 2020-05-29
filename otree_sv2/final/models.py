from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


class Constants(BaseConstants):
    name_in_url = 'final'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    chosen_task = models.IntegerField()

    def creating_session(self):
        self.chosen_task = self.session.vars['chosen_task']


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    def set_payoff(self):
        self.participant.payoff = self.participant.vars['task_payoffs'][self.subsession.chosen_task - 1]
