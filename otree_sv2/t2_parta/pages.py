from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Instructions(Page):
    pass


class Main(Page):
    form_model = 'player'

    def get_form_fields(self):
        return ['sp'+str(self.session.vars['s_order'][self.player.sp_count-1])]

    def before_next_page(self):
        self.player.sp_count += 1   # keeps track of which statement pair to display

        if self.player.sp_count == Constants.num_sp + 1:    # store the data when the statement pair pages are done
            pair_chosen = [self.player.sp1, self.player.sp2, self.player.sp3, self.player.sp4, self.player.sp5,
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
                s_pair = Constants.s_pairs[i].copy()
                self.participant.vars['sp_data'].append({
                    'index':                    i+1,
                    'original_statement':       s_pair.pop(pair_chosen[i]-1),
                    'opposite_statement':       s_pair.pop(),
                    'bid_amount':               None,
                })


page_sequence = [
    Instructions
] + [Main for i in range(Constants.num_sp)]
