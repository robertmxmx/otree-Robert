from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


class Constants(BaseConstants):
    name_in_url = 'oneRtwoGstart'
    players_per_group = 5
    num_rounds = 1

    stage1_instructions = 'oneRtwoGstart/Stage1InstructionsContent.html'
    stage2_instructions = 'oneRtwoGstart/Stage2InstructionsContent.html'
    stage3_instructions = 'oneRtwoGstart/Stage3InstructionsContent.html'

    comp_answers = {'c1': 1, 'c2': 2, 'c3': 1, 'c4': 1, 'c5': 3}


class Subsession(BaseSubsession):
    def get_task_number(self):
        this_task_order = self.session.config['app_sequence'].index('oneRtwoGstart')
        other_task_order = self.session.config['app_sequence'].index('twoRoneGstart')
        if this_task_order < other_task_order:
            return 1
        else:
            return 2


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    c1 = models.IntegerField(
        label="""Q1. If only one participant presses a green button, will the individual who lost 120 ECU be 
            restored to their original endowment?""",
        choices=[
            [1, 'Yes, the button-affected participant will have 120 ECU restored'],
            [2, 'No, both green buttons must be pressed for 120 ECU to be restored']
        ],
        widget=widgets.RadioSelect
    )
    c2 = models.IntegerField(
        label='Q2. If two participants press the green button, will anyone lose ECU?',
        choices=[
            [1, 'Yes, the individuals who press will each lose 40 ECU'],
            [2, 'Yes, the individuals who press will each lose 20 ECU'],
            [3, 'No, nobody loses ECU when the green button is pressed']
        ],
        widget=widgets.RadioSelect
    )
    c3 = models.IntegerField(
        label='Q3. How many players are selected to have the opportunity to press the red button?',
        choices=[1, 2, 3],
        widget=widgets.RadioSelect
    )
    c4 = models.IntegerField(
        label="""Q4. If two participants agree to assign 10 deduction points to another participant, how much will this 
              cost the participants who assign the points?""",
        choices=[
            [1, '5 ECU each'], [2, '10 ECU each'], [3, '30 ECU each'], [4, '30 ECU in total']
        ],
        widget=widgets.RadioSelect
    )
    c5 = models.IntegerField(
        label="""Q5. If a participant has 3 deduction points assigned to him or her, how many ECU will be deducted 
            from this participant?""",
        choices=[[1, '1.5 ECU'], [2, '3 ECU'], [3, '9 ECU'], [4, '30 ECU']],
        widget=widgets.RadioSelect
    )
    c1wrong = models.IntegerField(initial=0)
    c2wrong = models.IntegerField(initial=0)
    c3wrong = models.IntegerField(initial=0)
    c4wrong = models.IntegerField(initial=0)
    c5wrong = models.IntegerField(initial=0)
