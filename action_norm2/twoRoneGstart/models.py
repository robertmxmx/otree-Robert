from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


class Constants(BaseConstants):
    name_in_url = 'twoRoneGstart'
    players_per_group = 5
    num_rounds = 1

    stage1_instructions = 'twoRoneGstart/Stage1InstructionsContent.html'
    stage2_instructions = 'twoRoneGstart/Stage2InstructionsContent.html'
    stage3_instructions = 'twoRoneGstart/Stage3InstructionsContent.html'


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    c1 = models.IntegerField(
        label='Q1. If only one participant presses a red button, will anyone lose ECU?',
        choices=[
            [1, 'Yes, one participant will lose 120 ECU.'],
            [2, 'No, nobody loses ECU unless both red buttons are pressed.']
        ],
        widget=widgets.RadioSelect
    )
    c2 = models.IntegerField(
        label='Q2. If two participants press a red button, will anyone lose ECU?',
        choices=[
            [1, 'Yes, one participant will lose 120 ECU.'],
            [2, 'No, nobody loses ECU unless only one red button is pressed.']
        ],
        widget=widgets.RadioSelect
    )
    c3 = models.IntegerField(
        label='Q3. How many players are selected to have the opportunity to press the green button?',
        choices=[1, 2, 3],
        widget=widgets.RadioSelect
    )
    c4 = models.IntegerField(
        label='Q4. If two participants agree to assign 20 deduction points to another participant, how much will this cost the participants who assign the points?',
        choices=[
            [1, '10 ECU each'],
            [2, '20 ECU each'],
            [3, '60 ECU each'],
            [4, '60 ECU in total']
        ],
        widget=widgets.RadioSelect
    )
    c5 = models.IntegerField(
        label='Q5. If a participant has 3 deduction points assigned to him or her, how many ECU will be deducted from this participant?',
        choices=[
            [1, '1.5 ECU'],
            [2, '3 ECU'],
            [3, '6 ECU'],
            [4, '9 ECU']
        ],
        widget=widgets.RadioSelect
    )
    c1wrong = models.IntegerField(initial=0)
    c2wrong = models.IntegerField(initial=0)
    c3wrong = models.IntegerField(initial=0)
    c4wrong = models.IntegerField(initial=0)
    c5wrong = models.IntegerField(initial=0)
