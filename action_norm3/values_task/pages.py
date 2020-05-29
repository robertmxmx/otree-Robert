from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Instructions(Page):
    pass


class Main(Page):
    form_model = 'player'

    def get_form_fields(self):
        return ['sp%s' % str(self.player.sp_count)]

    def before_next_page(self):
        self.player.sp_count += 1


class Instructions2(Page):
    pass


class Main2(Page):
    form_model = 'player'

    def get_form_fields(self):
        return ['sp%s_accept' % str(self.player.sp_accept_count)]

    def vars_for_template(self):
        sp_choices = [self.player.sp1, self.player.sp2, self.player.sp3]
        sp = Constants.s_pairs[self.player.sp_accept_count-1].copy()
        original_statement = sp.pop(sp_choices[self.player.sp_accept_count-1]-1)
        opposite_statement = sp.pop()

        return {
            'original_statement': original_statement,
            'opposite_statement': opposite_statement
        }

    def before_next_page(self):
        self.player.sp_accept_count += 1


page_sequence = [Instructions] + [Main for i in range(Constants.num_sp)] + \
                [Instructions2] + [Main2 for i in range(Constants.num_sp)]
