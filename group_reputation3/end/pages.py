from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

def to_aud(amount, page):
    return c(amount).to_real_world_currency(page.session) if amount is not None else None

class End(Page):

    def is_displayed(self):
        return not self.participant.vars['droppedout'] and \
            'group' in self.participant.vars

    def vars_for_template(self):
        totalpayoff = 0
        bonus = None

        chosen_task = self.subsession.chosen_task
        task2_payoff = self.participant.vars['task2_payoffs'][chosen_task-1]
        totalpayoff += task2_payoff

        if 'bonus' in self.participant.vars:
            bonus = self.participant.vars['bonus']
            totalpayoff += bonus
        
        if 'survey_bonus' in self.participant.vars:
            surveybonus = self.participant.vars['survey_bonus']
            totalpayoff += surveybonus

        self.participant.payoff = c(totalpayoff)
        self.player.final_payoff = float(to_aud(totalpayoff, self))

        return {
            'chosen_task': chosen_task,
            'participation_fee': self.session.config['participation_fee'],
            'survey_bonus': to_aud(surveybonus, self),
            'task2_payoff': to_aud(task2_payoff, self),
            'bonus': to_aud(bonus, self)
        }
        

class UngroupedEnd(Page):

    def is_displayed(self):
        return not self.participant.vars['droppedout'] and \
            'group' not in self.participant.vars


page_sequence = [
    End,
    UngroupedEnd
]
