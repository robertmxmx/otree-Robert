from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


def create_html_table(d):
    content = '<table class="simple-table"><tr>'
    for key, value in dict(sorted(d.items())).items():
        content += '<th>%s</th>' % key
    content += '</tr><tr>'
    for key, value in dict(sorted(d.items())).items():
        content += '<td>%d</td>' % value
    content += '</tr></table>'

    return content

class Setup(WaitPage):
    group_by_arrival_time = True
    
    def after_all_players_arrive(self):
        self.group.init_round()


class Instructions(Page):

    def is_displayed(self):
        return self.round_number == 1


class Instructions2(Page):

    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        r_dict = self.player.get_instruction_vars()
        r_dict['show_init_msg'] = True
        r_dict['revealed'] = False
        return r_dict


class VideoInstructions(Page):

    def is_displayed(self):
        return self.round_number == 1


class Instructions3(Page):

    def is_displayed(self):
        return self.round_number == 1


class Instructions3a(Page):

    def is_displayed(self):
        return self.round_number == 1


class Instructions4(Page):

    def is_displayed(self):
        return self.round_number == 1


class Comprehension(Page):
    form_model = 'player'

    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        r_dict = self.player.get_instruction_vars()
        r_dict['show_init_msg'] = True
        r_dict['revealed'] = False
        return r_dict

    def get_form_fields(self):
        if self.session.config['rep_condition']:
            return ['comp1', 'comp2', 'comp3', 'comp4', 'comp5']
        else:
            return ['comp1', 'comp2', 'comp3', 'comp5']

    def error_message(self, values):
        errs = []
        # question 1
        if values['comp1'] != 1:
            errs.append('Question 1 is incorrect')
            self.player.comp1_wrong += 1
        # question 2
        if values['comp2'] is not True:
            errs.append('Question 2 is incorrect')
            self.player.comp2_wrong += 1
        # question 3
        if self.session.config['deterrence'] != values['comp3']:
            errs.append('Question 3 is incorrect')
            self.player.comp3_wrong += 1
        # question 4
        if self.session.config['rep_condition'] and values['comp4'] != 2:
            errs.append('Question 4 is incorrect')
            self.player.comp4_wrong += 1
        # question 5
        if values['comp5'] != 36:
            errs.append('Question 5 is incorrect')
            self.player.comp5_wrong += 1

        return errs


class Commencement(Page):
    pass


class TakingDecision(Page):
    form_model = 'player'
    form_fields = ['chose_to_take']

    def is_displayed(self):
        return self.player.role() == self.subsession.taking_player

    def vars_for_template(self):
        r_dict = self.player.get_instruction_vars()
        r_dict.update({
            'show_init_msg': False,
            'chose_to_take_label': "Do you wish to take %d of %s's ECU?" % (Constants.take_amount,
                                                                            self.subsession.deducting_player),
            'revealed': False
        })
        return r_dict


class DeductingDecision(Page):
    form_model = 'player'
    form_fields = ['deduct_amount']

    def is_displayed(self):
        return self.player.role() == self.subsession.deducting_player

    def vars_for_template(self):
        r_dict = self.player.get_instruction_vars()
        r_dict.update({
            'show_init_msg': False,
            'taking_player': self.subsession.taking_player,
            'revealed': False
        })
        return r_dict


class WaitingDecision(Page):
    form_model = 'player'
    
    def is_displayed(self):
        return self.player.role() not in [self.subsession.taking_player, self.subsession.deducting_player]

    def get_form_fields(self):
        if self.round_number == 1:
            return ['will_spend', 'should_spend']
        else:
            return ['will_spend_guess', 'should_spend_guess']


class CalculatePayoffs(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_payoffs()


class Feedback(Page):

    def vars_for_template(self):
        pat = {p.role(): int(p.payoff_after_take) for p in self.group.get_players()}
        fp = {p.role(): int(p.participant.payoff) for p in self.group.get_players()}
        tp = self.subsession.taking_player
        dp = self.subsession.deducting_player
        ecu_taken = self.group.get_player_by_role(tp).chose_to_take
        da = int(self.group.get_player_by_role(dp).deduct_amount)
        mult_da = int(Constants.deduct['multiplier'] * da)

        if self.round_number == 1:
            # set feedback content. this is done here so that it can be retrieved in the next round
            ta = Constants.take_amount

            content = ""
            if ecu_taken:
                content += '<p>%s decided to take %d ECU from %s</p>' % (tp, ta, dp)
            else:
                content += '<p>%s decided not to take %d ECU from %s</p>' % (tp, ta, dp)
            content += '<p>This led to the following distribution of endowments:</p>'
            content += create_html_table(pat)
            if ecu_taken:
                content += '''<p>%s chose to spend %d ECU on deductions. This had the effect of reducing %s's 
                    endowment by %d ECU, and reducing %s's endowment by %d ECU''' % (dp, da, tp, mult_da, dp, da)
            content += '<p>Final earnings for this task are:</p>'
            content += create_html_table(fp)

            self.participant.vars['task2a_feedback'] = content
            return {'task2a_feedback': content}
        else:
            return {
                'task2a_feedback': self.participant.vars['task2a_feedback'],
                'receiving_info': self.player.role() in [tp, dp],
                'points_were_taken': ecu_taken,
                'taking_player': tp, 'deducting_player': dp,
                'payoffs_after_take': dict(sorted(pat.items())),
                'deduct_amount': da, 'multiplied_deduct_amount': mult_da,
                'final_payoffs': dict(sorted(fp.items()))
            }

    def before_next_page(self):
        p = self.participant
        if 'task2_payoffs' not in p.vars:
            p.vars['task2_payoffs'] = []
        p.vars['task2_payoffs'].append(p.payoff)

class CMessage(Page):

    def is_displayed(self):
        return self.session.config['rep_condition'] and self.round_number == 2
    
    def vars_for_template(self):
        r_dict = self.player.get_instruction_vars()
        r_dict['show_init_msg'] = False
        r_dict['revealed'] = True
        return r_dict
    

page_sequence = [
    Setup,

    Instructions,
    Instructions2,
    VideoInstructions,
    Instructions3,
    Instructions3a,
    Instructions4,

    Comprehension,

    Commencement,

    TakingDecision,
    DeductingDecision,
    WaitingDecision,

    CalculatePayoffs,
    Feedback,

    CMessage
]
