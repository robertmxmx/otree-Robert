from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Summary(Page):
    def vars_for_template(self):
        self.participant.payoff = 0
        self.player.t1_payoff = c(self.participant.vars['summary_data'][0][1]).to_real_world_currency(self.session)
        self.player.t2_payoff = c(self.participant.vars['summary_data'][1][1]).to_real_world_currency(self.session)
        self.player.t3_payoff = c(self.participant.vars['summary_data'][2][1]).to_real_world_currency(self.session)
        self.player.t4_payoff = c(self.participant.vars['summary_data'][3][1]).to_real_world_currency(self.session)
        self.player.t5_payoff = c(self.participant.vars['summary_data'][4][1]).to_real_world_currency(self.session)
        return {
            'summary_data': self.participant.vars['summary_data']
        }


class Final(Page):
    def vars_for_template(self):
        chosen1_payoff = c(self.participant.vars['summary_data'][self.group.chosen1 - 1][1]).to_real_world_currency(self.session)
        chosen2_payoff = c(self.participant.vars['summary_data'][self.group.chosen2 - 1][1]).to_real_world_currency(self.session)
        part_fee = self.session.config['participation_fee']
        self.player.total = c(chosen1_payoff + chosen2_payoff + part_fee).to_real_world_currency(self.session)

        return_dict = {
            'chosen_task1': self.group.chosen1,
            'chosen_task2': self.group.chosen2,
            'payoff1': chosen1_payoff,
            'payoff2': chosen2_payoff,
            'part_fee': part_fee,
            'total': self.player.total
        }

        if self.group.chosen1 == 3 or self.group.chosen2 == 3:
            if self.group.chosen1 == 3:
                self.player.total_no3 = c(chosen2_payoff + part_fee).to_real_world_currency(self.session)
            elif self.group.chosen2 == 3:
                self.player.total_no3 = c(chosen1_payoff + part_fee).to_real_world_currency(self.session)
            return_dict.update({
                'total_no3': self.player.total_no3
            })

        return return_dict


page_sequence = [
    Summary,
    Final,
]
