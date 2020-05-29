from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random
import shared


class Constants(BaseConstants):
    name_in_url = 'twoRoneG'
    players_per_group = 5
    num_rounds = shared.num_rounds

    initial_ECUs = [180, 200, 220]
    p_ids = ['A', 'B', 'C', 'D', 'E']
    max_deduction_points = 10
    sp_options = {
        'none': """to assign zero deduction points""",
        'r': """to assign the maximum possible deduction points to the red presser (10 points assigned to the
            red presser)""",
        'rs': """to assign the maximum possible deduction points to the red pressers (10 points assigned to 
            each red presser)""",
        'r_only': """to assign the maximum possible deduction points to the red pressers only (10 points assigned 
            to each red presser)""",
        'g_only': """to assign the maximum possible deduction points to the green non-presser only (10 points 
            assigned to the green non-presser)""",
        'r_and_g': """to assign equal number of points to each red presser and each green non-presser (10 points 
            per red presser and 10 points for the green non-presser)""",
        'all_pols': """I would agree to any of the above three policies, if they were proposed (Green only, 
            Red only, Both)""",
        'no_pols': """I would not agree to any of the above three deduction policies (Green only, Red only, Both)""",
        'comb_pols': """I would agree to some other combination of policies not described above."""
    }
    sp_questions = {
        'sp_pressed_red': """Q1. If you are chosen to have the opportunity to press the red button in stage 1, 
        will you press it?""",
        'sp_pressed_green': """Q2. If stage 2 occurs (because two participants pressed the red button), and you 
        are chosen to have the opportunity to press a green button, will you press it?""",
        'sp_unaff_1r': """Q3. Scenario 'One red'. If stage 3 occurs, where only one red button has been pressed, 
        and you are the unaffected participant, which of the following deduction policies would you support?""",
        'sp_unaff_2r1g': """Q4. Scenario 'Two red, one green'. If stage 3 occurs, where only both red buttons 
        have been pressed, and you are the unaffected participant, which of the following deduction policies would 
        you support?""",
        'sp_unaff_2r0g': """Q5. Scenario 'Two red, no green'. If stage 3 occurs, where only both red buttons 
        have been pressed, and you are the unaffected participant, which of the following deduction policies would 
        you support?""",
        'sp_aff_1r': """Q6. Scenario 'One red'. If stage 3 occurs, where only one red button has been pressed, 
        and you are the button-affected participant, which of the following deduction policies would you agree to?""",
        'sp_aff_2r1g': """Q7. Scenario 'Two red, one green'. If stage 3 occurs, where only both red buttons 
        have been pressed, and you are the button-affected participant, which of the following deduction policies 
        would you support?""",
        'sp_aff_2r0g': """Q8. Scenario 'Two red, no green'. If stage 3 occurs, where only both red buttons 
        have been pressed, and you are the button-affected participant, which of the following deduction policies 
        would you support?""",
    }
    exp_bonus = 25


class Subsession(BaseSubsession):

    def creating_session(self):
        if self.round_number == 1:
            self.group_randomly()
        else:
            self.group_like_round(1)

        for group in self.get_groups():
            players = group.get_players()           # this will shuffle the groups so that
            random.shuffle(players)                 # p_prev_id_in_group is not necessarily
            group.set_players(players)              # equal to p_id_in_group

    def this_page_active(self, page, player, group):                            # this helps determine whether the
        sp_round_active = (self.round_number == self.session.config['sp_round_num'])         # given page should be displayed or not
        r1_playing = (player == group.get_player_by_role('red_presser1'))
        r2_playing = (player == group.get_player_by_role('red_presser2'))
        r_count = group.num_red_pressed
        g_playing = (player == group.get_player_by_role('green_presser'))
        unaff_playing = (player == group.get_player_by_role('unaffected'))
        aff_playing = (player == group.get_player_by_role('affected'))

        if page == "SpecialRoundInstructions" or page == "SpecialRound" or page == "WaitSpecialRound":
            return sp_round_active
        elif page == "Stage1Decision":
            return not sp_round_active and (r1_playing or r2_playing)
        elif page == "Stage2Decision":
            return not sp_round_active and r_count == 2 and g_playing
        elif page == "Feedback":
            return not sp_round_active or (sp_round_active and r_count == 0)
        elif page == "Stage3Decision":
            return not sp_round_active and r_count != 0 and unaff_playing
        elif page == "WaitStage3Decision":
            return not sp_round_active and r_count != 0
        elif page == "Stage3Agreement":
            return not sp_round_active and r_count != 0 and aff_playing
        elif page == "Stage3Feedback":
            return r_count != 0
        elif page == "ExpectationSurvey" or page == "WaitExpectation" or page == "ExpectationEnd":
            return self.round_number == self.session.config['exp_round_num']
        elif page == "WaitFinal" or page == "ExpectationFeedback":
            return self.round_number == Constants.num_rounds
        else:
            print("ERROR")


class Group(BaseGroup):
    num_red_pressed = models.IntegerField()
    exp_question_picked = models.IntegerField(initial=random.choice([1, 2, 3]))
    exp_majority_answer = models.StringField()
    exp_tie = models.BooleanField()

    def initialise_game(self):
        p_ids = Constants.p_ids.copy()
        random.shuffle(p_ids)
        for p in self.get_players():
            p.initial_ECU = random.choice(Constants.initial_ECUs)       # set initial earnings and
            p.p_id = p_ids.pop()                                        # IDS for each player

    def set_stage1_actions(self):
        r1 = self.get_player_by_role('red_presser1')
        r2 = self.get_player_by_role('red_presser2')

        if r1.pressed_red and r2.pressed_red:
            aff = self.get_player_by_role('affected')
            self.num_red_pressed = 2
            r1.stage1_ECU = r1.initial_ECU + 20
            r2.stage1_ECU = r2.initial_ECU + 20
            aff.stage1_ECU = aff.initial_ECU - 120
        elif r1.pressed_red:
            self.num_red_pressed = 1
            r1.stage1_ECU = r1.initial_ECU + 40
        elif r2.pressed_red:
            self.num_red_pressed = 1
            r2.stage1_ECU = r2.initial_ECU + 40
        else:
            self.num_red_pressed = 0

        others = [p for p in self.get_players() if p.stage1_ECU is None]
        for p in others:
            p.stage1_ECU = p.initial_ECU

    def set_stage2_actions(self):
        g = self.get_player_by_role('green_presser')

        if g.pressed_green:
            aff = self.get_player_by_role('affected')
            g.stage2_ECU = g.stage1_ECU - 40
            aff.stage2_ECU = aff.stage1_ECU + 120

        others = [p for p in self.get_players() if p.stage2_ECU is None]
        for p in others:
            p.stage2_ECU = p.stage1_ECU

    def set_stage3_actions(self):
        aff = self.get_player_by_role('affected')

        if aff.accepted_deduction:
            r1 = self.get_player_by_role('red_presser1')
            r2 = self.get_player_by_role('red_presser2')
            g = self.get_player_by_role('green_presser')
            unaff = self.get_player_by_role('unaffected')
            x = unaff.red_d_pts
            y = unaff.green_d_pts
            n = self.num_red_pressed
            aff.stage3_ECU = aff.stage2_ECU - (((n * x) + y) / 2)
            unaff.stage3_ECU = unaff.stage2_ECU - (((n * x) + y) / 2)
            r1.stage3_ECU = (r1.stage2_ECU - (3 * x) if r1.pressed_red else r1.stage2_ECU)
            r2.stage3_ECU = (r2.stage2_ECU - (3 * x) if r2.pressed_red else r2.stage2_ECU)
            g.stage3_ECU = g.stage2_ECU - (3 * y)

        others = [p for p in self.get_players() if p.stage3_ECU is None]
        for p in others:
            p.stage3_ECU = p.stage2_ECU

    def get_stage2_feedback(self):
        r1 = self.get_player_by_role('red_presser1')
        r2 = self.get_player_by_role('red_presser2')
        aff = self.get_player_by_role('affected')
        g = self.get_player_by_role('green_presser')
        pressed, not_pressed = self.get_who_pressed([r1, r2])

        return {
            'initial_payoffs': self.get_payoffs('initial'),
            'red_presser1': r1.p_id,
            'red_presser2': r2.p_id,
            'p_pressed_red': and_formatter(pressed),
            'p_not_pressed_red': and_formatter(not_pressed),
            'num_red_pressed': self.num_red_pressed,
            'affected': aff.p_id,
            'green_presser': g.p_id,
            'green_pressed': 'chose' if g.pressed_green else 'declined',
            'stage2_payoffs': self.get_payoffs('stage2'),
        }

    def get_who_pressed(self, pressers):        # this will return a tuple of pressers
        pressed = []                            # that actually pressed the red button
        not_pressed = []                        # and those that did not

        for p in pressers:
            if p.pressed_red:
                pressed.append(p.p_id)
            else:
                not_pressed.append(p.p_id)

        return pressed, not_pressed

    def handle_sp_round(self):                              # this should handle all the logic for the
        r1 = self.get_player_by_role('red_presser1')        # special round
        r2 = self.get_player_by_role('red_presser2')
        g = self.get_player_by_role('green_presser')
        aff = self.get_player_by_role('affected')
        unaff = self.get_player_by_role('unaffected')

        r1.pressed_red = r1.sp_pressed_red
        r2.pressed_red = r2.sp_pressed_red

        pressed, not_pressed = self.get_who_pressed([r1, r2])

        if len(pressed) == 1:
            unaff.red_d_pts = (10 if unaff.sp_unaff_1r == 1 else 0)
            unaff.green_d_pts = 0

            if aff.sp_aff_1r == 1 and unaff.sp_unaff_1r == 1:
                aff.accepted_deduction = True
            else:
                aff.accepted_deduction = False

        elif len(pressed) == 2:
            g.pressed_green = g.sp_pressed_green

            if g.pressed_green:
                unaff.red_d_pts = (10 if unaff.sp_unaff_2r1g == 1 else 0)
                unaff.green_d_pts = 0

                if aff.sp_aff_2r1g == 1 and unaff.sp_unaff_2r1g == 1:
                    aff.accepted_deduction = True
                else:
                    aff.accepted_deduction = False

            elif not g.pressed_green:
                unaff.red_d_pts = (10 if unaff.sp_unaff_2r0g in [1, 3] else 0)
                unaff.green_d_pts = (10 if unaff.sp_unaff_2r0g in [2, 3] else 0)

                if unaff.sp_unaff_2r0g in [1, 2, 3] and \
                    (aff.sp_aff_2r0g in [unaff.sp_unaff_2r0g, 4] or
                        (aff.sp_aff_2r0g == 6 and random.random() < (2 / 3))):
                    aff.accepted_deduction = True               # handles the question when
                else:                                           # the player can a pick a
                    aff.accepted_deduction = False              # combination of policies

    def get_payoffs(self, type):
        td = []                                             # table data

        for p in self.get_players():                        # get ids and payoffs
            if type == 'initial':                           # for the table on this page
                td.append({'id': p.p_id, 'payoff': p.initial_ECU})
            elif type == 'stage2':
                td.append({'id': p.p_id, 'payoff': p.stage2_ECU})
            elif type == 'final':
                td.append({'id': p.p_id, 'payoff': p.stage3_ECU})

        return sorted(td, key=lambda k: k['id'])


class Player(BasePlayer):
    p_id = models.StringField()
    initial_ECU = models.FloatField()
    pressed_red = models.BooleanField()
    stage1_ECU = models.FloatField()
    pressed_green = models.BooleanField()
    stage2_ECU = models.FloatField()
    red_d_pts = models.FloatField(min=0, max=Constants.max_deduction_points,)
    green_d_pts = models.FloatField(min=0, max=Constants.max_deduction_points,)
    accepted_deduction = models.BooleanField()
    stage3_ECU = models.FloatField()
    sp_pressed_red = models.BooleanField(label=Constants.sp_questions['sp_pressed_red'])          # special round variables
    sp_pressed_green = models.BooleanField(label=Constants.sp_questions['sp_pressed_green'])
    sp_unaff_1r = models.IntegerField(
        label=Constants.sp_questions['sp_unaff_1r'],
        choices=[[1, Constants.sp_options['r']], [2, Constants.sp_options['none']]],
        widget=widgets.RadioSelect
    )
    sp_unaff_2r1g = models.IntegerField(
        label=Constants.sp_questions['sp_unaff_2r1g'],
        choices=[[1, Constants.sp_options['rs']], [2, Constants.sp_options['none']]],
        widget=widgets.RadioSelect
    )
    sp_unaff_2r0g = models.IntegerField(
        label=Constants.sp_questions['sp_unaff_2r0g'],
        choices=[[1, Constants.sp_options['r_only']], [2, Constants.sp_options['g_only']],
                 [3, Constants.sp_options['r_and_g']], [4, Constants.sp_options['none']]],
        widget=widgets.RadioSelect
    )
    sp_aff_1r = models.IntegerField(
        label=Constants.sp_questions['sp_aff_1r'],
        choices=[[1, Constants.sp_options['r']], [2, Constants.sp_options['none']]],
        widget=widgets.RadioSelect
    )
    sp_aff_2r1g = models.IntegerField(
        label=Constants.sp_questions['sp_aff_2r1g'],
        choices=[[1, Constants.sp_options['rs']], [2, Constants.sp_options['none']]],
        widget=widgets.RadioSelect
    )
    sp_aff_2r0g = models.IntegerField(
        label=Constants.sp_questions['sp_aff_2r0g'],
        choices=[
            [1, "(Red only) I would agree " + Constants.sp_options['r_only']],
            [2, "(Green only) I would agree " + Constants.sp_options['g_only']],
            [3, "(Both) I would agree " + Constants.sp_options['r_and_g']],
            [4, Constants.sp_options['all_pols']],
            [5, Constants.sp_options['no_pols']],
            [6, Constants.sp_options['comb_pols']]
        ],
        widget=widgets.RadioSelect
    )
    exp1 = models.IntegerField(label="", choices=[1, 2, 3, 4, 5])             # expectation survey variables
    exp2 = models.IntegerField(label="", choices=[1, 2, 3, 4, 5])
    exp3 = models.IntegerField(
        label="",
        choices=[
            [1, '10 deduction points assigned to each red presser and to the green non-presser'],
            [2, '10 deduction points assigned to each red presser, and zero assigned to the green non-presser'],
            [3, '10 deduction points assigned to the green non-presser, and zero assigned to each red presser']
        ],
        widget=widgets.RadioSelect
    )
    exp_ECU = models.FloatField()

    def role(self):
        id = self.id_in_group
        if id == 1:
            return 'red_presser1'
        elif id == 2:
            return 'red_presser2'
        elif id == 3:
            return 'green_presser'
        elif id == 4:
            return 'affected'
        else:
            return 'unaffected'


def and_formatter(li):
    '''
    Formats a string with 'and' between elements
    :param li: list of elements
    :return: string in format of: 'li[0] and li[1] and ...'
    '''
    if len(li) == 0:
        return ""
    else:
        string = str(li[0])
        for elem in li[1:]:
            string += " and %s" % elem
        return string
