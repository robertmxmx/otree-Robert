from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import random


class AllWait(WaitPage):
    wait_for_all_groups = True


class PartAInstructions(Page):
    pass


class PartA(Page):
    form_model = 'player'

    def get_form_fields(self):
        return ['sp'+str(self.player.sp_count)]

    def before_next_page(self):
        self.player.sp_count += 1   # keeps of track of which statement pair to display

        if self.player.sp_count == Constants.num_sp + 1:    # store the data when the statement pair pages are done
            temp = [self.player.sp1, self.player.sp2, self.player.sp3, self.player.sp4, self.player.sp5,
                    self.player.sp6, self.player.sp7, self.player.sp8, self.player.sp9, self.player.sp10,
                    self.player.sp11, self.player.sp12, self.player.sp13, self.player.sp14, self.player.sp15,
                    self.player.sp16, self.player.sp17, self.player.sp18, self.player.sp19, self.player.sp20,
                    self.player.sp21, self.player.sp22, self.player.sp23, self.player.sp24, self.player.sp25,
                    self.player.sp26, self.player.sp27, self.player.sp28, self.player.sp29, self.player.sp30,
                    self.player.sp31, self.player.sp32, self.player.sp33, self.player.sp34, self.player.sp35,
                    self.player.sp36, self.player.sp37, self.player.sp38, self.player.sp39, self.player.sp40,
                    self.player.sp41, self.player.sp42, self.player.sp43, self.player.sp44, self.player.sp45,
                    self.player.sp46, self.player.sp47, self.player.sp48, self.player.sp49, self.player.sp50,
                    self.player.sp51, self.player.sp52, self.player.sp53, self.player.sp54, self.player.sp55,
                    self.player.sp56, self.player.sp57, self.player.sp58, self.player.sp59, self.player.sp60,
                    self.player.sp61, self.player.sp62]

            for i in range(Constants.num_sp):
                temp2 = Constants.s_pairs[i].copy()
                self.participant.vars['sp_data'].append([temp2.pop(temp[i]-1), None])
                self.participant.vars['sp_data'][-1].append(temp2.pop())


class PartBInstructions(Page):
    pass


class PartB(Page):
    form_model = 'player'

    def get_form_fields(self):
        return ['sp'+str(self.player.sp_bid_count)+'_bid']

    def vars_for_template(self):
        sp_index = self.player.sp_bid_count - 1
        return {
            'accepted_statement': self.participant.vars['sp_data'][sp_index][0],
            'to_accept_statement': self.participant.vars['sp_data'][sp_index][2]
        }

    def error_message(self, values):
        correct_input = [str(i) for i in range(Constants.min_bid, Constants.max_bid + 1)]
        correct_input.append(Constants.opt_out_text)
        if values['sp'+str(self.player.sp_bid_count)+'_bid'] not in correct_input:
            return 'Amount must be number from 1-100 or "' + Constants.opt_out_text + '"'

    def before_next_page(self):
        self.player.sp_bid_count += 1   # keeps track of which statement pair bid page we are on

        if self.player.sp_bid_count == Constants.num_sp + 1:    # store data when finished with bid pages
            temp = [self.player.sp1_bid, self.player.sp2_bid, self.player.sp3_bid, self.player.sp4_bid,
                    self.player.sp5_bid, self.player.sp6_bid, self.player.sp7_bid, self.player.sp8_bid,
                    self.player.sp9_bid, self.player.sp10_bid, self.player.sp11_bid, self.player.sp12_bid,
                    self.player.sp13_bid, self.player.sp14_bid, self.player.sp15_bid, self.player.sp16_bid,
                    self.player.sp17_bid, self.player.sp18_bid, self.player.sp19_bid, self.player.sp20_bid,
                    self.player.sp21_bid, self.player.sp22_bid, self.player.sp23_bid, self.player.sp24_bid,
                    self.player.sp25_bid, self.player.sp26_bid, self.player.sp27_bid, self.player.sp28_bid,
                    self.player.sp29_bid, self.player.sp30_bid, self.player.sp31_bid, self.player.sp32_bid,
                    self.player.sp33_bid, self.player.sp34_bid, self.player.sp35_bid, self.player.sp36_bid,
                    self.player.sp37_bid, self.player.sp38_bid, self.player.sp39_bid, self.player.sp40_bid,
                    self.player.sp41_bid, self.player.sp42_bid, self.player.sp43_bid, self.player.sp44_bid,
                    self.player.sp45_bid, self.player.sp46_bid, self.player.sp47_bid, self.player.sp48_bid,
                    self.player.sp49_bid, self.player.sp50_bid, self.player.sp51_bid, self.player.sp52_bid,
                    self.player.sp53_bid, self.player.sp54_bid, self.player.sp55_bid, self.player.sp56_bid,
                    self.player.sp57_bid, self.player.sp58_bid, self.player.sp59_bid, self.player.sp60_bid,
                    self.player.sp61_bid, self.player.sp62_bid]

            for i in range(Constants.num_sp):  # store statements chosen and bids for each statement
                if temp[i] == Constants.opt_out_text:
                    self.participant.vars['sp_data'][i][1] = 'Opt out'
                else:
                    self.participant.vars['sp_data'][i][1] = temp[i]
                self.participant.vars['sp_data'][i].pop()


class PartBOutcome(Page):

    def vars_for_template(self):
        return self.player.set_payoff()

    def before_next_page(self):
        sp_data = []

        for sp in self.participant.vars['sp_data']:
            if sp[1] == 'Opt out':
                sp_data.append(sp[0] + " (" + sp[1] + ")")
            else:
                sp_data.append(sp[0] + " ($" + sp[1] + ")")

        self.participant.vars['sp_data'] = sp_data
        if 'summary_data' in self.participant.vars:
            self.participant.vars['summary_data'].append(('Task 3', self.participant.payoff))


page_sequence = [
    AllWait,

    PartAInstructions,
    PartA, PartA, PartA, PartA, PartA, PartA, PartA, PartA, PartA, PartA, PartA, PartA, PartA, PartA, PartA, PartA,
    PartA, PartA, PartA, PartA, PartA, PartA, PartA, PartA, PartA, PartA, PartA, PartA, PartA, PartA, PartA, PartA,
    PartA, PartA, PartA, PartA, PartA, PartA, PartA, PartA, PartA, PartA, PartA, PartA, PartA, PartA, PartA, PartA,
    PartA, PartA, PartA, PartA, PartA, PartA, PartA, PartA, PartA, PartA, PartA, PartA, PartA, PartA,

    PartBInstructions,
    PartB, PartB, PartB, PartB, PartB, PartB, PartB, PartB, PartB, PartB, PartB, PartB, PartB, PartB, PartB, PartB,
    PartB, PartB, PartB, PartB, PartB, PartB, PartB, PartB, PartB, PartB, PartB, PartB, PartB, PartB, PartB, PartB,
    PartB, PartB, PartB, PartB, PartB, PartB, PartB, PartB, PartB, PartB, PartB, PartB, PartB, PartB, PartB, PartB,
    PartB, PartB, PartB, PartB, PartB, PartB, PartB, PartB, PartB, PartB, PartB, PartB, PartB, PartB,
    PartBOutcome
]
