from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random


class Constants(BaseConstants):
    name_in_url = 'oneRtwoG'
    players_per_group = 5
    num_rounds = 2

    sp_round_num = random.randint(1, num_rounds)    # round when there will be a special round



class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    r_presser = models.StringField()            # red button presser
    r_affected = models.StringField()           # participant affected by the red button
    g1_presser = models.StringField()           # first green button presser
    g2_presser = models.StringField()           # second green button presser
    unaffected = models.StringField()           # participant that was unaffected
    g_pressers = models.StringField()
    g_decliners = models.StringField()
    num_g_pressed = models.IntegerField()
    r_pressed = models.BooleanField(
        label='Do you wish to press the red button?'
    )
    g1_pressed = models.BooleanField(
        label='Do you wish to press the green button?'
    )
    g2_pressed = models.BooleanField(
        label='Do you wish to press the green button?'
    )
    r_deduction_pts = models.CurrencyField(
        label='How many deduction points do you wish to assign to the red button presser?',
        min=0, max=30,
    )
    g_deduction_pts = models.CurrencyField(
        label='How many deduction points do you wish to assign to each green button non-presser (if there was one)?',
        min=0, max=30,
    )
    deduction_accepted = models.BooleanField()

    def initialise_game(self):
        # assign roles to participants
        ids = ['A', 'B', 'C', 'D', 'E']
        random.shuffle(ids)
        for p in self.get_players():
            p.player_id = ids.pop()
        # assign which role does what
        ids = ['A', 'B', 'C', 'D', 'E']
        random.shuffle(ids)
        self.r_presser = ids.pop()
        self.r_affected = ids.pop()
        self.g1_presser = ids.pop()
        self.g2_presser = ids.pop()
        self.unaffected = ids.pop()
        for p in self.get_players():
            p.payoff = 200

    def set_green_pressers_decliners(self):
        if self.g1_pressed and self.g2_pressed:         # both pressed green
            self.num_g_pressed = 2
            self.g_pressers = self.g1_presser + " and " + self.g2_presser
            self.g_decliners = ""
        elif self.g1_pressed and not self.g2_pressed:   # first green presser pressed
            self.num_g_pressed = 1
            self.g_pressers = self.g1_presser
            self.g_decliners = self.g2_presser
        elif not self.g1_pressed and self.g2_pressed:   # second green presser pressed
            self.num_g_pressed = 1
            self.g_pressers = self.g2_presser
            self.g_decliners = self.g1_presser
        else:                                                       # nobody pressed green
            self.num_g_pressed = 0
            self.g_pressers = ""
            self.g_decliners = self.g1_presser + " and " + self.g2_presser

    def set_button_payoffs(self):
        if self.r_pressed:                          # red button is pressed
            for p in self.get_players():
                if p.player_id == self.r_presser:
                    p.payoff += 40
                elif p.player_id == self.r_affected:
                    p.payoff -= 120

        for p in self.get_players():                # set stage 1 earnings
            p.stage1_earnings = p.payoff

        for p in self.get_players():                # give 40 ECU to participants that can press the green button
            if p.player_id == self.g1_presser or p.player_id == self.g2_presser:
                p.payoff += 40

        if self.g1_pressed or self.g2_pressed:      # at least one green button is pressed
            for p in self.get_players():
                if p.player_id == self.g1_presser or p.player_id == self.g2_presser:
                    p.payoff -= 40
                elif p.player_id == self.r_affected:
                    p.payoff += 120

        for p in self.get_players():                # set stage 1 earnings
            p.stage2_earnings = p.payoff

    def set_deduction_points(self):
        for p in self.get_players():
            if p.player_id == self.r_affected or p.player_id == self.unaffected:
                p.payoff -= (self.r_deduction_pts + (2-self.num_g_pressed) * self.g_deduction_pts) / 2
            elif p.player_id == self.r_presser:
                p.payoff -= 3 * self.r_deduction_pts
            elif p.player_id == self.g1_presser and not self.g1_pressed:
                p.payoff -= 3 * self.g_deduction_pts
            elif p.player_id == self.g2_presser and not self.g2_pressed:
                p.payoff -= 3 * self.g_deduction_pts

    def set_special_payoff(self):
        for p in self.get_players():
            if p.player_id == self.r_presser:
                self.r_pressed = True if p.r_pressed else False
            elif p.player_id == self.g1_presser:
                self.g1_pressed = True if p.g_pressed else False
            elif p.player_id == self.g2_presser:
                self.g2_pressed = True if p.g_pressed else False

        self.set_button_payoffs()

        if self.r_pressed:
            self.set_green_pressers_decliners()
            aff_arr = []
            un_arr = []

            for p in self.get_players():
                if p.player_id == self.unaffected:
                    un_arr = [p.d_un_r0g, p.d_un_r1g, p.d_un_r2g]
                elif p.player_id == self.r_affected:
                    aff_arr = [p.d_aff_r0g, p.d_aff_r1g, p.d_aff_r2g]

            if self.num_g_pressed == 0:
                if un_arr[0] == aff_arr[0]:
                    self.deduction_accepted = True
                    if un_arr == 1:
                        self.r_deduction_pts = 30
                        self.g_deduction_pts = 0
                    elif un_arr == 2:
                        self.r_deduction_pts = 0
                        self.g_deduction_pts = 15
                    else:
                        self.r_deduction_pts = 10
                        self.g_deduction_pts = 10
                else:
                    self.deduction_accepted = False
                    self.r_deduction_pts = 0
                    self.g_deduction_pts = 0
            elif self.num_g_pressed == 1:
                if un_arr[1] == aff_arr[1]:
                    self.deduction_accepted = True
                    if un_arr == 1:
                        self.r_deduction_pts = 30
                        self.g_deduction_pts = 0
                    elif un_arr == 2:
                        self.r_deduction_pts = 0
                        self.g_deduction_pts = 30
                    else:
                        self.r_deduction_pts = 15
                        self.g_deduction_pts = 15
                else:
                    self.deduction_accepted = False
                    self.r_deduction_pts = 0
                    self.g_deduction_pts = 0
            else:
                if un_arr[2] == aff_arr[2]:
                    self.deduction_accepted = True
                    self.r_deduction_pts = 30
                    self.g_deduction_pts = 0
                else:
                    self.deduction_accepted = False
                    self.r_deduction_pts = 0
                    self.g_deduction_pts = 0

            self.set_deduction_points()


class Player(BasePlayer):
    player_id = models.StringField()
    stage1_earnings = models.CurrencyField()
    stage2_earnings = models.CurrencyField()
    # special round variables
    r_pressed = models.BooleanField(
        label='Q1. If you are chosen to have the opportunity to press the red button in stage 1, will you press it?'
    )
    g_pressed = models.BooleanField(
        label='Q2. If stage 2 occurs (because someone pressed the red button), and you are chosen to have the opportunity to press a green button, will you press it?'
    )
    d_un_r0g = models.IntegerField(    # Deduction policy for UNaffected when Red button is pressed and 0 Green buttons are pressed
        label='Q3. Scenario “One red, no green”. If stage 3 occurs, where only the red button was pressed, and you are the unaffected participant, which of the following deduction policies would you support?',
        choices=[
            [1, 'to assign the maximum possible deduction points to the red presser only (30 points assigned to the red presser)'],
            [2, 'to assign the maximum possible deduction points to the green non-pressers only (15 points assigned to each green non-presser)'],
            [3, 'to assign equal number of points to the red presser and each green refuser (10 points for red presser and 10 points per green refuser)'],
            [4, 'to assign zero deduction points']
        ],
        widget=widgets.RadioSelect
    )
    d_un_r1g = models.IntegerField(
        label='Q4. Scenario “One red, one green”. If stage 3 occurs, where the red button was pressed and one green button was pressed, and you are the unaffected participant, which of the following deduction policies would you support?',
        choices=[
            [1, 'to assign the maximum possible deduction points to the red presser (30 points assigned to the red presser)'],
            [2, 'to assign the maximum possible deduction points to the green non-presser only (30 points assigned to the green non-presser)'],
            [3, 'to assign equal number of points to the red presser and the green refuser (15 points for red presser and 15 points for green refuser)'],
            [4, 'to assign zero deduction points']
        ],
        widget=widgets.RadioSelect
    )
    d_un_r2g = models.IntegerField(
        label='Q5. Scenario “One red, two green”. If stage 3 occurs, where the red button was pressed and both green buttons were pressed, and you are the unaffected participant, which of the following deduction policies would you support?',
        choices=[
            [1, 'to assign the maximum possible deduction points to the red presser (30 points assigned to the red presser)'],
            [2, 'to assign zero deduction points']
        ],
        widget=widgets.RadioSelect
    )
    d_aff_r0g = models.IntegerField(
        label='Q6. Scenario “One red, no green”. If stage 3 occurs, where only the red button was pressed, and you are the button-affected participant, which of the following deduction policies would you agree to? (Select all applicable)',
        choices=[
            [1, 'to assign the maximum possible deduction points to the red presser only (30 points assigned to the red presser)'],
            [2, 'to assign the maximum possible deduction points to the green non-pressers only (15 points assigned to each green non-presser)'],
            [3, 'to assign equal number of points to the red presser and each green refuser (10 points for red presser and 10 points per green refuser)']
        ],
        widget=widgets.RadioSelect
    )
    d_aff_r1g = models.IntegerField(
        label='Q7. Scenario “One red, one green”. If stage 3 occurs, where the red button was pressed and one green button was pressed, and you are the button-affected participant, which of the following deduction policies would you agree to? (Select all applicable)',
        choices=[
            [1, 'to assign the maximum possible deduction points to the red presser (30 points assigned to the red presser)'],
            [2, 'to assign the maximum possible deduction points to the green non-presser only (30 points assigned to the green non-presser)'],
            [3, 'to assign equal number of points to each red presser and the green refuser (15 points for red presser and 15 points for green refuser)']
        ],
        widget=widgets.RadioSelect
    )
    d_aff_r2g = models.IntegerField(
        label='Q8. Scenario “One red, two green”. If stage 3 occurs, where the red button was pressed and both green buttons were pressed, and you are the button-affected participant, which of the following deduction policies would you agree to?',
        choices=[
            [1, 'to assign the maximum possible deduction points to the red presser (30 points assigned to the red presser)']
        ],
        widget=widgets.RadioSelect
    )