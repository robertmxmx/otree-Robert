from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import random


class Instructions(Page):
    pass


class Main(Page):
    form_model = 'player'

    def get_form_fields(self):
        return ['sp'+str(self.session.vars['s_order'][self.player.sp_bid_count-1])+'_bid']

    def vars_for_template(self):
        sp_info = self.participant.vars['sp_data'][self.session.vars['s_order'][self.player.sp_bid_count-1]-1]
        return {
            'original_statement': sp_info['original_statement'],
            'opposite_statement': sp_info['opposite_statement']
        }

    def error_message(self, values):
        correct_input = [str(i) for i in range(Constants.min_bid, Constants.max_bid + 1)] + [Constants.opt_out_text]

        if values['sp'+str(self.session.vars['s_order'][self.player.sp_bid_count-1])+'_bid'] not in correct_input:
            return 'Amount must be a number from %s to %s or "%s"' % (Constants.min_bid, Constants.max_bid, Constants.opt_out_text)

    def before_next_page(self):
        self.player.sp_bid_count += 1   # keeps track of which statement pair bid page we are on

        if self.player.sp_bid_count == Constants.num_sp + 1:    # store data when finished with bid pages
            bids = [self.player.sp1_bid, self.player.sp2_bid, self.player.sp3_bid, self.player.sp4_bid,
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

            sp_data = self.participant.vars['sp_data'].copy()

            for i in range(Constants.num_sp):  # store statements chosen and bids for each statement
                if bids[i] == Constants.opt_out_text:
                    sp_data[i]['bid_amount'] = Constants.opt_out_text
                else:
                    sp_data[i]['bid_amount'] = int(bids[i])

            self.participant.vars['sp_data'] = sp_data.copy()

            self.player.set_payoff()
            self.player.change_out_value()


class Outcome(Page):

    def before_next_page(self):
        string = """
            <h5>
                Task 2 Earnings
            </h5>
            <p>
                We randomly selected the following statement for payment: %s
            </p>
            <p>
                Your lowest acceptable price to accept the opposite statement was: %s
            </p>
            <p>
                Our randomly generated switching price was: %s
            </p>
        """ % (self.participant.vars['sp_data'][self.player.chosen_statement - 1]['original_statement'],
               "Opt out" if self.player.bid_amount == Constants.opt_out_text else c(int(self.player.bid_amount)).to_real_world_currency(self.session),
               self.player.gen_amount.to_real_world_currency(self.session))

        if self.player.task_payoff == c(0):
            string += """
                <p>
                    Therefore, you will not receive payment for this task, and you will not be asked to sign the
                    opposite statement.
                </p>
            """
        else:
            string += """
                <p>
                    Therefore you will be paid %s for this task, in exchange for signing
                    the opposite statement
                </p>
            """ % self.player.task_payoff.to_real_world_currency(self.session)

        self.participant.vars['task_outcomes'].append(string)


page_sequence = [Instructions] + [Main for i in range(Constants.num_sp)] + [Outcome]
