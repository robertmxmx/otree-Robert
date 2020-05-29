from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random
import shared


class Constants(BaseConstants):
    name_in_url = 'start'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    paid_task = models.IntegerField()
    paid_round = models.IntegerField()

    def creating_session(self):
        if 'oneRtwoG' in self.session.config['app_sequence'] or 'twoRoneG' in self.session.config['app_sequence']:
            paid_task_name = random.choice(['twoRoneG', 'oneRtwoG'])
            oneRtwoG_order = self.session.config['app_sequence'].index('oneRtwoG')
            twoRoneG_order = self.session.config['app_sequence'].index('twoRoneG')

            if oneRtwoG_order < twoRoneG_order:
                paid_task_num = (1 if paid_task_name == 'oneRtwoG' else 2)
            else:
                paid_task_num = (1 if paid_task_name == 'twoRoneG' else 2)

            self.paid_task = paid_task_num
            self.paid_round = random.choice(list(range(1, shared.num_rounds+1)))
            self.session.vars['paid_task_name'] = paid_task_name
            self.session.vars['paid_task'] = self.paid_task
            self.session.vars['paid_round'] = self.paid_round
        else:
            self.paid_task = 1
            self.paid_round = random.choice(list(range(1, shared.num_rounds+1)))
            self.session.vars['paid_task_name'] = 'twoRtwoG'
            self.session.vars['paid_task'] = self.paid_task
            self.session.vars['paid_round'] = self.paid_round



class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass
