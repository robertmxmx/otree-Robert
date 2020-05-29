from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random, os, time


class Constants(BaseConstants):
    name_in_url = 't2_partb'
    players_per_group = None
    num_rounds = 1

    instructions_content = 't2_partb/InstructionsContent.html'
    num_sp = 62
    min_bid = 1
    max_bid = 50
    opt_out_text = 'out'


class Subsession(BaseSubsession):
    def creating_session(self):
        for p in self.get_players():
            p.chosen_statement = random.randint(1, Constants.num_sp)
            p.gen_amount = random.randint(Constants.min_bid, Constants.max_bid)


class Group(BaseGroup):
    pass


def create_sp_bid():
    return models.StringField(label="Your bid:")


class Player(BasePlayer):
    sp_bid_count = models.IntegerField(initial=1)   # determines which statement to bid against
    # Players entered bids for each statements
    sp1_bid = create_sp_bid()
    sp2_bid = create_sp_bid()
    sp3_bid = create_sp_bid()
    sp4_bid = create_sp_bid()
    sp5_bid = create_sp_bid()
    sp6_bid = create_sp_bid()
    sp7_bid = create_sp_bid()
    sp8_bid = create_sp_bid()
    sp9_bid = create_sp_bid()
    sp10_bid = create_sp_bid()
    sp11_bid = create_sp_bid()
    sp12_bid = create_sp_bid()
    sp13_bid = create_sp_bid()
    sp14_bid = create_sp_bid()
    sp15_bid = create_sp_bid()
    sp16_bid = create_sp_bid()
    sp17_bid = create_sp_bid()
    sp18_bid = create_sp_bid()
    sp19_bid = create_sp_bid()
    sp20_bid = create_sp_bid()
    sp21_bid = create_sp_bid()
    sp22_bid = create_sp_bid()
    sp23_bid = create_sp_bid()
    sp24_bid = create_sp_bid()
    sp25_bid = create_sp_bid()
    sp26_bid = create_sp_bid()
    sp27_bid = create_sp_bid()
    sp28_bid = create_sp_bid()
    sp29_bid = create_sp_bid()
    sp30_bid = create_sp_bid()
    sp31_bid = create_sp_bid()
    sp32_bid = create_sp_bid()
    sp33_bid = create_sp_bid()
    sp34_bid = create_sp_bid()
    sp35_bid = create_sp_bid()
    sp36_bid = create_sp_bid()
    sp37_bid = create_sp_bid()
    sp38_bid = create_sp_bid()
    sp39_bid = create_sp_bid()
    sp40_bid = create_sp_bid()
    sp41_bid = create_sp_bid()
    sp42_bid = create_sp_bid()
    sp43_bid = create_sp_bid()
    sp44_bid = create_sp_bid()
    sp45_bid = create_sp_bid()
    sp46_bid = create_sp_bid()
    sp47_bid = create_sp_bid()
    sp48_bid = create_sp_bid()
    sp49_bid = create_sp_bid()
    sp50_bid = create_sp_bid()
    sp51_bid = create_sp_bid()
    sp52_bid = create_sp_bid()
    sp53_bid = create_sp_bid()
    sp54_bid = create_sp_bid()
    sp55_bid = create_sp_bid()
    sp56_bid = create_sp_bid()
    sp57_bid = create_sp_bid()
    sp58_bid = create_sp_bid()
    sp59_bid = create_sp_bid()
    sp60_bid = create_sp_bid()
    sp61_bid = create_sp_bid()
    sp62_bid = create_sp_bid()
    chosen_statement = models.IntegerField()
    bid_amount = models.StringField()
    gen_amount = models.CurrencyField()
    task_payoff = models.CurrencyField()

    def set_payoff(self):
        accepted_statement = self.participant.vars['sp_data'][self.chosen_statement - 1]['opposite_statement']
        bid_amount = self.participant.vars['sp_data'][self.chosen_statement - 1]['bid_amount']
        self.bid_amount = str(bid_amount)
        gen_amount = self.gen_amount

        if bid_amount == Constants.opt_out_text:
            self.task_payoff = c(0)
        else:
            if c(bid_amount) <= gen_amount:
                self.task_payoff = gen_amount
                self.print_accepted_statement(accepted_statement, gen_amount)
            else:
                self.task_payoff = c(0)

        self.participant.vars['task_payoffs'].append(self.task_payoff)

    def print_accepted_statement(self, statement, price):
        with open(os.path.abspath('output_files/' + self.session.code + '_p'+str(self.participant.id_in_session)+'.html'), 'w') as f:
            f.write("""
                <html>
                    <h1>Monash Laboratory for Experimental Economics</h1>
                    <body style="text-align: center;">
                        <h2>Participant statement</h2>
                        <p>Participant number: %s</p>
                        <br/>
                        <p>I accept the following statement:</p>
                        <p>
                            <strong>
                                %s (%s)
                            </strong>
                        </p>
                        <br/>
                        <br/>
                        <p>Print name: __________________________</p>
                        <br/>
                        <p>Signed: __________________________ Date: ________</p>
                    </body>
                </html>
            """ % (self.participant.id_in_session, statement, price.to_real_world_currency(self.session)))

    def change_out_value(self):
        if self.sp1_bid == Constants.opt_out_text:
            self.sp1_bid = "101"
        if self.sp2_bid == Constants.opt_out_text:
            self.sp2_bid = "101"
        if self.sp3_bid == Constants.opt_out_text:
            self.sp3_bid = "101"
        if self.sp4_bid == Constants.opt_out_text:
            self.sp4_bid = "101"
        if self.sp5_bid == Constants.opt_out_text:
            self.sp5_bid = "101"
        if self.sp6_bid == Constants.opt_out_text:
            self.sp6_bid = "101"
        if self.sp7_bid == Constants.opt_out_text:
            self.sp7_bid = "101"
        if self.sp8_bid == Constants.opt_out_text:
            self.sp8_bid = "101"
        if self.sp9_bid == Constants.opt_out_text:
            self.sp9_bid = "101"
        if self.sp10_bid == Constants.opt_out_text:
            self.sp10_bid = "101"
        if self.sp11_bid == Constants.opt_out_text:
            self.sp11_bid = "101"
        if self.sp12_bid == Constants.opt_out_text:
            self.sp12_bid = "101"
        if self.sp13_bid == Constants.opt_out_text:
            self.sp13_bid = "101"
        if self.sp14_bid == Constants.opt_out_text:
            self.sp14_bid = "101"
        if self.sp15_bid == Constants.opt_out_text:
            self.sp15_bid = "101"
        if self.sp16_bid == Constants.opt_out_text:
            self.sp16_bid = "101"
        if self.sp17_bid == Constants.opt_out_text:
            self.sp17_bid = "101"
        if self.sp18_bid == Constants.opt_out_text:
            self.sp18_bid = "101"
        if self.sp19_bid == Constants.opt_out_text:
            self.sp19_bid = "101"
        if self.sp20_bid == Constants.opt_out_text:
            self.sp20_bid = "101"
        if self.sp21_bid == Constants.opt_out_text:
            self.sp21_bid = "101"
        if self.sp22_bid == Constants.opt_out_text:
            self.sp22_bid = "101"
        if self.sp23_bid == Constants.opt_out_text:
            self.sp23_bid = "101"
        if self.sp24_bid == Constants.opt_out_text:
            self.sp24_bid = "101"
        if self.sp25_bid == Constants.opt_out_text:
            self.sp25_bid = "101"
        if self.sp26_bid == Constants.opt_out_text:
            self.sp26_bid = "101"
        if self.sp27_bid == Constants.opt_out_text:
            self.sp27_bid = "101"
        if self.sp28_bid == Constants.opt_out_text:
            self.sp28_bid = "101"
        if self.sp29_bid == Constants.opt_out_text:
            self.sp29_bid = "101"
        if self.sp30_bid == Constants.opt_out_text:
            self.sp30_bid = "101"
        if self.sp31_bid == Constants.opt_out_text:
            self.sp31_bid = "101"
        if self.sp32_bid == Constants.opt_out_text:
            self.sp32_bid = "101"
        if self.sp33_bid == Constants.opt_out_text:
            self.sp33_bid = "101"
        if self.sp34_bid == Constants.opt_out_text:
            self.sp34_bid = "101"
        if self.sp35_bid == Constants.opt_out_text:
            self.sp35_bid = "101"
        if self.sp36_bid == Constants.opt_out_text:
            self.sp36_bid = "101"
        if self.sp37_bid == Constants.opt_out_text:
            self.sp37_bid = "101"
        if self.sp38_bid == Constants.opt_out_text:
            self.sp38_bid = "101"
        if self.sp39_bid == Constants.opt_out_text:
            self.sp39_bid = "101"
        if self.sp40_bid == Constants.opt_out_text:
            self.sp40_bid = "101"
        if self.sp41_bid == Constants.opt_out_text:
            self.sp41_bid = "101"
        if self.sp42_bid == Constants.opt_out_text:
            self.sp42_bid = "101"
        if self.sp43_bid == Constants.opt_out_text:
            self.sp43_bid = "101"
        if self.sp44_bid == Constants.opt_out_text:
            self.sp44_bid = "101"
        if self.sp45_bid == Constants.opt_out_text:
            self.sp45_bid = "101"
        if self.sp46_bid == Constants.opt_out_text:
            self.sp46_bid = "101"
        if self.sp47_bid == Constants.opt_out_text:
            self.sp47_bid = "101"
        if self.sp48_bid == Constants.opt_out_text:
            self.sp48_bid = "101"
        if self.sp49_bid == Constants.opt_out_text:
            self.sp49_bid = "101"
        if self.sp50_bid == Constants.opt_out_text:
            self.sp50_bid = "101"
        if self.sp51_bid == Constants.opt_out_text:
            self.sp51_bid = "101"
        if self.sp52_bid == Constants.opt_out_text:
            self.sp52_bid = "101"
        if self.sp53_bid == Constants.opt_out_text:
            self.sp53_bid = "101"
        if self.sp54_bid == Constants.opt_out_text:
            self.sp54_bid = "101"
        if self.sp55_bid == Constants.opt_out_text:
            self.sp55_bid = "101"
        if self.sp56_bid == Constants.opt_out_text:
            self.sp56_bid = "101"
        if self.sp57_bid == Constants.opt_out_text:
            self.sp57_bid = "101"
        if self.sp58_bid == Constants.opt_out_text:
            self.sp58_bid = "101"
        if self.sp59_bid == Constants.opt_out_text:
            self.sp59_bid = "101"
        if self.sp60_bid == Constants.opt_out_text:
            self.sp60_bid = "101"
        if self.sp61_bid == Constants.opt_out_text:
            self.sp61_bid = "101"
        if self.sp62_bid == Constants.opt_out_text:
            self.sp62_bid = "101"
