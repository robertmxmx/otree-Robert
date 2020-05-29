from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class WaitInitial(WaitPage):

    def after_all_players_arrive(self):
        self.group.initialise_game()


class Beginning(Page):

    def vars_for_template(self):
        return {'initial_payoffs': self.group.get_payoffs('initial')}


class SpecialRoundInstructions(Page):

    def is_displayed(self):
        return self.subsession.this_page_active("SpecialRoundInstructions", self.player, self.group)


class SpecialRound(Page):
    form_model = 'player'
    form_fields = ['sp_pressed_red', 'sp_pressed_green', 'sp_unaff_0g', 'sp_unaff_1g', 'sp_unaff_2g',
                   'sp_aff_0g', 'sp_aff_1g', 'sp_aff_2g']

    def is_displayed(self):
        return self.subsession.this_page_active("SpecialRound", self.player, self.group)

    def vars_for_template(self):
        return {'initial_payoffs': self.group.get_payoffs('initial')}


class WaitSpecialRound(WaitPage):

    def is_displayed(self):
        return self.subsession.this_page_active("WaitSpecialRound", None, self.group)

    def after_all_players_arrive(self):
        self.group.handle_sp_round()


class Stage1Decision(Page):
    form_model = 'player'
    form_fields = ['pressed_red']

    def is_displayed(self):
        return self.subsession.this_page_active("Stage1Decision", self.player, self.group)


class WaitStage1Decision(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_stage1_actions()


class Stage2Decision(Page):
    form_model = 'player'
    form_fields = ['pressed_green']

    def is_displayed(self):
        return self.subsession.this_page_active("Stage2Decision", self.player, self.group)

    def vars_for_template(self):
        return {'red_presser': self.group.get_player_by_role('red_presser').p_id}


class WaitStage2Decision(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_stage2_actions()


class Feedback(Page):

    def is_displayed(self):
        return self.subsession.this_page_active("Feedback", self.player, self.group)

    def vars_for_template(self):
        return self.group.get_stage2_feedback()


class Stage3Decision(Page):
    form_model = 'player'
    form_fields = ['red_d_pts', 'green_d_pts']

    def is_displayed(self):
        return self.subsession.this_page_active("Stage3Decision", self.player, self.group)

    def error_message(self, values):
        if self.group.num_green_not_pressed == 0 and values['green_d_pts'] != 0:
            return "0 points must be assigned to green button non-pressers as both green buttons were pressed"


class WaitStage3Decision(WaitPage):

    def is_displayed(self):
        return self.subsession.this_page_active("WaitStage3Decision", None, self.group)


class Stage3Agreement(Page):
    form_model = 'player'

    def get_form_fields(self):
        x = self.group.get_player_by_role('unaffected').red_d_pts
        y = self.group.get_player_by_role('unaffected').green_d_pts
        if x == 0 and y == 0:
            return []
        else:
            return ['accepted_deduction']

    def is_displayed(self):
        return self.subsession.this_page_active("Stage3Agreement", self.player, self.group)

    def vars_for_template(self):
        x = self.group.get_player_by_role('unaffected').red_d_pts
        y = self.group.get_player_by_role('unaffected').green_d_pts
        n = self.group.num_green_not_pressed
        return {
            'red_d_pts': x,
            'green_d_pts': y,
            'cost_to_me': (x + (n * y)) / 2,
            'red_d_pts_x3': 3 * x,
            'green_d_pts_x3': 3 * y,
        }


class WaitStage3Agreement(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_stage3_actions()


class Stage3Feedback(Page):

    def is_displayed(self):
        return self.subsession.this_page_active("Stage3Feedback", self.player, self.group)

    def vars_for_template(self):
        unaff = self.group.get_player_by_role('unaffected')
        aff = self.group.get_player_by_role('affected')
        stage2_feedback = self.group.get_stage2_feedback()
        return_dict = {
            'red_d_pts': unaff.red_d_pts,
            'green_d_pts': unaff.green_d_pts,
            'accepted_deduction': 'accepted' if aff.accepted_deduction else 'rejected',
            'final_payoffs': self.group.get_payoffs('final'),
            'unaff_id': unaff.p_id
        }

        return_dict.update(stage2_feedback)

        return return_dict


class ExpectationSurvey(Page):
    form_model = 'player'
    form_fields = ['exp1', 'exp2', 'exp3']

    def is_displayed(self):
        return self.subsession.this_page_active("ExpectationSurvey", self.player, self.group)


class ExpectationEnd(Page):

    def is_displayed(self):
        return self.subsession.this_page_active("ExpectationEnd", self.player, self.group)


class WaitExpectation(WaitPage):

    def is_displayed(self):
        return self.subsession.this_page_active("WaitExpectation", None, self.group)

    def after_all_players_arrive(self):
        exp_answer_count = {}
        all_exp_answers = []
        exp_question_picked = self.group.exp_question_picked - 1

        for p in self.group.get_players():                      # store all the players answers to expectation survey in
            all_exp_answers.append([p.exp1, p.exp2, p.exp3])    # array: [[p1_q1, p1_q2, p1_q3], [p2_q1, p2_q2, p2_q3], ...]

        for p_answers in all_exp_answers:                   # count how many times an answer was chosen for
            choice = str(p_answers[exp_question_picked])    # the chosen question and store in dictionary:
            if choice in exp_answer_count:                  # {answer1: num_votes, answer2: num_votes, ...}
                exp_answer_count[choice] += 1
            else:
                exp_answer_count[choice] = 1

        mva = max(exp_answer_count, key=exp_answer_count.get)                   # most voted for answer
        num_voted_for_mva = exp_answer_count[mva]

        if num_voted_for_mva >= (int(Constants.players_per_group / 2) + 1):     # find if majority voted for mva,
            self.group.exp_tie = False
            self.group.exp_majority_answer = mva
            for p in self.group.get_players():                                  # pay those that voted for mva
                p_answers = [p.exp1, p.exp2, p.exp3]
                if p_answers[exp_question_picked] == int(mva):
                    p.exp_ECU = Constants.exp_bonus
                else:
                    p.exp_ECU = 0
        else:
            self.group.exp_tie = True
            for p in self.group.get_players():
                p.exp_ECU = 0

        for p in self.group.get_players():
            p.participant.vars['exp_data'] = {
                'tie': self.group.exp_tie,
                'question_picked': self.group.exp_question_picked,
                'majority_answer': self.group.exp_majority_answer,
                'exp_ECU': p.exp_ECU
            }


class ExpectationFeedback(Page):

    def is_displayed(self):
        return self.subsession.this_page_active("ExpectationFeedback", self.player, self.group)

    def vars_for_template(self):
        exp_data = self.participant.vars['exp_data']

        return {
            'tie': exp_data['tie'],
            'question_picked': exp_data['question_picked'],
            'majority_answer': exp_data['majority_answer'],
            'exp_ECU': exp_data['exp_ECU']
        }


class WaitFinal(WaitPage):

    def is_displayed(self):
        return self.subsession.this_page_active("WaitFinal", None, self.group)

    def after_all_players_arrive(self):
        for p in self.group.get_players():
            exp_rn = self.session.config['exp_round_num']
            expectations_survey_earnings = p.in_round(exp_rn).exp_ECU

            if 'expectations_survey_earnings' in p.participant.vars:
                p.participant.vars['expectations_survey_earnings'] += expectations_survey_earnings
            else:
                p.participant.vars['expectations_survey_earnings'] = expectations_survey_earnings

            p.payoff += c(expectations_survey_earnings)
        if self.session.vars['paid_task_name'] == Constants.name_in_url:
            rn = self.session.vars['paid_round']
            for p in self.group.get_players():
                main_exp_earnings = p.in_round(rn).stage3_ECU

                p.participant.vars['main_exp_earnings'] = main_exp_earnings
                p.payoff += c(main_exp_earnings)


page_sequence = [
    WaitInitial,
    Beginning,

    SpecialRoundInstructions,
    SpecialRound,
    WaitSpecialRound,

    Stage1Decision,
    WaitStage1Decision,

    Stage2Decision,
    WaitStage2Decision,
    Feedback,

    Stage3Decision,
    WaitStage3Decision,
    Stage3Agreement,
    WaitStage3Agreement,
    Stage3Feedback,

    ExpectationSurvey,
    ExpectationEnd,
    WaitExpectation,
    ExpectationFeedback,

    WaitFinal
]
