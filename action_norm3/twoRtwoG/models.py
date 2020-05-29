from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random
import shared


class Constants(BaseConstants):
    name_in_url = 'twoRtwoG'
    players_per_group = 6
    num_rounds = shared.num_rounds

    comp_answers = {'c1': 2, 'c2': 1, 'c3': 2, 'c4': 1, 'c5': 2, 'c6': 1, 'c7': 3}

    initial_ECUs = [180, 200, 220]
    p_ids = ['A', 'B', 'C', 'D', 'E', 'F']

    sp_options = {}  # fixme
    sp_questions = {}

    exp_bonus = 25

    one_red_btn_gain = 40
    two_red_btn_gain = 20
    two_red_btn_loss = 120

    one_green_btn_loss = 40
    one_green_btn_gain = 120
    two_green_btn_loss = 20
    two_green_btn_gain = 120

    deduction_multiplier = 3
    max_deduction_points = 10


class Subsession(BaseSubsession):

    def creating_session(self):
        if self.round_number == 1:
            self.group_randomly()
        else:
            self.group_like_round(1)

        for group in self.get_groups():
            players = group.get_players()  # this will shuffle players within groups
            random.shuffle(players)
            group.set_players(players)

    def get_task_number(self):
        return 1

    def this_page_active(self, page, player, group):  # this helps determine whether the
        # sp_round_active = (self.round_number == self.session.config['sp_round_num'])
        sp_round_active = False     # fixme
        r1_playing = (player == group.get_player_by_role('r1'))
        r2_playing = (player == group.get_player_by_role('r2'))
        r_count = group.num_red_pressed
        g1_playing = (player == group.get_player_by_role('g1'))
        g2_playing = (player == group.get_player_by_role('g2'))
        unaff_playing = (player == group.get_player_by_role('unaff'))
        aff_playing = (player == group.get_player_by_role('aff'))

        if page in ["Start", "Stage1Instructions", "Stage2Instructions", "Stage3Instructions",
                    "ComprehensionQuestions"]:
            return self.round_number == 1
        elif page in ["SpecialRoundInstructions", "SpecialRound", "WaitSpecialRound"]:
            return sp_round_active
        elif page == "Stage1Decision":
            return not sp_round_active and (r1_playing or r2_playing)
        elif page == "Stage2Decision":
            return not sp_round_active and r_count == 2 and (g1_playing or g2_playing)
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
        elif page in ["ExpectationSurvey", "WaitExpectation", "ExpectationEnd"]:
            return self.round_number == self.session.config['exp_round_num']
        elif page == "WaitFinal" or page == "ExpectationFeedback":
            return self.round_number == Constants.num_rounds
        else:
            print("ERROR")


class Group(BaseGroup):
    num_red_pressed = models.IntegerField()
    num_green_not_pressed = models.IntegerField()
    exp_question_picked = models.IntegerField(initial=random.choice([1, 2, 3]))
    exp_majority_answer = models.StringField()
    exp_tie = models.BooleanField()

    def initialise_game(self):
        p_ids = Constants.p_ids.copy()
        random.shuffle(p_ids)
        for p in self.get_players():
            p.initial_ECU = random.choice(Constants.initial_ECUs)  # set initial earnings and
            p.p_id = p_ids.pop()  # IDS for each player

    def get_who_pressed(self, pressers, button):  # this will return a tuple of pressers
        pressed = []  # that actually pressed the red button
        not_pressed = []  # and those that did not

        for p in pressers:
            if button == 'red':
                if p.pressed_red:
                    pressed.append(p.p_id)
                else:
                    not_pressed.append(p.p_id)
            elif button == 'green':
                if p.pressed_green:
                    pressed.append(p.p_id)
                else:
                    not_pressed.append(p.p_id)

        return pressed, not_pressed

    def get_payoffs(self, type):
        td = []  # table data

        for p in self.get_players():  # get ids and payoffs
            if type == 'initial':  # for the table on this page
                td.append({'id': p.p_id, 'payoff': p.initial_ECU})
            elif type == 'stage2':
                td.append({'id': p.p_id, 'payoff': p.stage2_ECU})
            elif type == 'final':
                td.append({'id': p.p_id, 'payoff': p.stage3_ECU})

        return sorted(td, key=lambda k: k['id'])

    def set_stage1_actions(self):
        r1 = self.get_player_by_role('r1')
        r2 = self.get_player_by_role('r2')

        if r1.pressed_red and r2.pressed_red:
            aff = self.get_player_by_role('aff')
            self.num_red_pressed = 2
            r1.stage1_ECU = r1.initial_ECU + Constants.two_red_btn_gain
            r2.stage1_ECU = r2.initial_ECU + Constants.two_red_btn_gain
            aff.stage1_ECU = aff.initial_ECU - Constants.two_red_btn_loss
        elif r1.pressed_red:
            self.num_red_pressed = 1
            r1.stage1_ECU = r1.initial_ECU + Constants.one_red_btn_gain
        elif r2.pressed_red:
            self.num_red_pressed = 1
            r2.stage1_ECU = r2.initial_ECU + Constants.one_red_btn_gain
        else:
            self.num_red_pressed = 0

        others = [p for p in self.get_players() if p.stage1_ECU is None]
        for p in others:
            p.stage1_ECU = p.initial_ECU

    def set_stage2_actions(self):
        g1 = self.get_player_by_role('g1')
        g2 = self.get_player_by_role('g2')
        aff = self.get_player_by_role('aff')

        if g1.pressed_green and g2.pressed_green:
            self.num_green_not_pressed = 0
            g1.stage2_ECU = g1.stage1_ECU - Constants.two_green_btn_loss
            g2.stage2_ECU = g2.stage1_ECU - Constants.two_green_btn_loss
            aff.stage2_ECU = aff.stage1_ECU + Constants.two_green_btn_gain
        elif g1.pressed_green:
            self.num_green_not_pressed = 1
            g1.stage2_ECU = g1.stage1_ECU - Constants.one_green_btn_loss
            aff.stage2_ECU = aff.stage1_ECU + Constants.one_green_btn_gain
        elif g2.pressed_green:
            self.num_green_not_pressed = 1
            g2.stage2_ECU = g2.stage1_ECU - Constants.one_green_btn_loss
            aff.stage2_ECU = aff.stage1_ECU + Constants.one_green_btn_gain
        else:
            self.num_green_not_pressed = 2

        others = [p for p in self.get_players() if p.stage2_ECU is None]
        for p in others:
            p.stage2_ECU = p.stage1_ECU

    def get_stage2_feedback(self):
        r_pressers = [self.get_player_by_role('r1'), self.get_player_by_role('r2')]
        aff = self.get_player_by_role('aff')
        g_pressers = [self.get_player_by_role('g1'), self.get_player_by_role('g2')]
        pressed_red, not_pressed_red = self.get_who_pressed(r_pressers, 'red')
        pressed_green, not_pressed_green = self.get_who_pressed(g_pressers, 'green')

        return {
            'initial_payoffs': self.get_payoffs('initial'),
            'red_pressers': shared.format_list([_.p_id for _ in r_pressers], 'and'),
            'p_pressed_red': shared.format_list(pressed_red, 'and'),
            'p_not_pressed_red': shared.format_list(not_pressed_red, 'and'),
            'num_red_pressed': self.num_red_pressed,
            'affected': aff.p_id,
            'green_pressers': shared.format_list([_.p_id for _ in g_pressers], 'and'),
            'p_pressed_green': shared.format_list(pressed_green, 'and'),
            'p_not_pressed_green': shared.format_list(not_pressed_green, 'and'),
            'num_green_pressed': self.num_green_not_pressed,
            'stage2_payoffs': self.get_payoffs('stage2'),
        }

    def set_stage3_actions(self):
        aff = self.get_player_by_role('aff')

        if aff.accepted_deduction:
            r1 = self.get_player_by_role('r1')
            r2 = self.get_player_by_role('r2')
            g1 = self.get_player_by_role('g1')
            g2 = self.get_player_by_role('g2')
            unaff = self.get_player_by_role('unaff')
            x = unaff.red_d_pts
            y = unaff.green_d_pts
            n1 = self.num_red_pressed
            n2 = self.num_green_not_pressed
            aff.stage3_ECU = aff.stage2_ECU - (((n1 * x) + (n2 * y)) / 2)
            unaff.stage3_ECU = unaff.stage2_ECU - (((n1 * x) + (n2 * y)) / 2)
            r1.stage3_ECU = (r1.stage2_ECU - (Constants.deduction_multiplier * x) if r1.pressed_red else r1.stage2_ECU)
            r2.stage3_ECU = (r2.stage2_ECU - (Constants.deduction_multiplier * x) if r2.pressed_red else r2.stage2_ECU)
            g1.stage3_ECU = (g1.stage2_ECU - (Constants.deduction_multiplier * y) if not g1.pressed_green else g1.stage2_ECU)
            g2.stage3_ECU = (g2.stage2_ECU - (Constants.deduction_multiplier * y) if not g2.pressed_green else g2.stage2_ECU)

        others = [p for p in self.get_players() if p.stage3_ECU is None]
        for p in others:
            p.stage3_ECU = p.stage2_ECU

    def handle_sp_round(self):  # fixme
        pass


class Player(BasePlayer):
    c1 = models.IntegerField(
        label="""If only one participant presses a red button, will anyone lose ECU?""",
        choices=[
            [1, 'Yes, one participant will lose 120 ECU'],
            [2, 'No, nobody loses ECU unless both red buttons are pressed']
        ],
        widget=widgets.RadioSelect
    )
    c2 = models.IntegerField(
        label="""If two participants press a red button, will anyone lose ECU?""",
        choices=[
            [1, 'Yes, one participant will lose 120 ECU'],
            [2, 'No, nobody loses ECU unless only one red button is pressed']
        ],
        widget=widgets.RadioSelect
    )
    c3 = models.IntegerField(
        label="""How many players are selected to have the opportunity to press a green button?""",
        choices=[1, 2, 3],
        widget=widgets.RadioSelect
    )
    c4 = models.IntegerField(
        label="""If only one participant presses a green button, will the individual who lost 120 ECU
            be restored to 200 ECU?""",
        choices=[
            [1, 'Yes, the button-affected participant will have 120 ECU restored'],
            [2, 'No, both green buttons must be pressed for 120 ECU to be restored']
        ],
        widget=widgets.RadioSelect
    )
    c5 = models.IntegerField(
        label="""If two participants press a green button, will anyone lose ECU?""",
        choices=[
            [1, 'Yes, the individuals who press will each lose 40 ECU'],
            [2, 'Yes, the individuals who press will each lose 20 ECU'],
            [3, 'No, nobody loses ECU when a green button is pressed']
        ],
        widget=widgets.RadioSelect
    )
    c6 = models.IntegerField(
        label="""If two participants agree to assign 10 deduction points to another participant, how
            much will this cost the participants who assign the points?""",
        choices=[
            [1, '5 ECU each'],
            [2, '10 ECU each'],
            [3, '30 ECU each'],
            [4, '15 ECU in total']
        ],
        widget=widgets.RadioSelect
    )
    c7 = models.IntegerField(
        label="""If a participant has 3 deduction points assigned to him or her, how many ECU will be
            deducted from this participant?""",
        choices=[
            [1, '1.5 ECU'],
            [2, '3 ECU'],
            [3, '9 ECU'],
            [4, '30 ECU']
        ],
        widget=widgets.RadioSelect
    )
    c1wrong = models.IntegerField(initial=0)
    c2wrong = models.IntegerField(initial=0)
    c3wrong = models.IntegerField(initial=0)
    c4wrong = models.IntegerField(initial=0)
    c5wrong = models.IntegerField(initial=0)
    c6wrong = models.IntegerField(initial=0)
    c7wrong = models.IntegerField(initial=0)
    p_id = models.StringField()
    initial_ECU = models.FloatField()
    pressed_red = models.BooleanField(label="Do you wish to press the red button?")
    stage1_ECU = models.FloatField()
    pressed_green = models.BooleanField(label="Do you wish to press the green button?")
    stage2_ECU = models.FloatField()
    red_d_pts = models.FloatField(
        label="How many deduction points do you wish to assign to each red button presser?",
        min=0, max=Constants.max_deduction_points
    )
    green_d_pts = models.FloatField(
        label="How many deduction points do you wish to assign to each green button non-presser (if there were any)?",
        min=0, max=Constants.max_deduction_points
    )
    accepted_deduction = models.BooleanField()
    stage3_ECU = models.FloatField()
    sp_pressed_red = models.BooleanField()  # special round variables fixme
    sp_pressed_green = models.BooleanField()
    sp_unaff_0g = models.IntegerField()
    sp_unaff_1g = models.IntegerField()
    sp_unaff_2g = models.IntegerField()
    sp_aff_0g = models.IntegerField()
    sp_aff_1g = models.IntegerField()
    sp_aff_2g = models.IntegerField()
    exp1 = models.IntegerField(label="", choices=[1, 2, 3, 4, 5])  # expectation survey variables
    exp2 = models.IntegerField(label="", choices=[1, 2, 3, 4, 5])
    exp3 = models.IntegerField(
        label="",
        choices=[
            [1, '10 deduction points assigned to each red presser and to each green non-presser'],
            [2, '10 deduction points assigned to each red presser, and zero assigned to each green non-presser'],
            [3, '10 deduction points assigned to each green non-presser, and zero assigned to each red presser']
        ],
        widget=widgets.RadioSelect
    )
    exp_ECU = models.FloatField()

    def role(self):
        id = self.id_in_group
        if id == 1:
            return 'r1'
        elif id == 2:
            return 'r2'
        elif id == 3:
            return 'g1'
        elif id == 4:
            return 'g2'
        elif id == 5:
            return 'aff'
        else:
            return 'unaff'
