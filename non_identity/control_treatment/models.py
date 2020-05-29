from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random, os

author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'control_treatment'
    players_per_group = None
    num_rounds = 1

    t1_instructions_content = 'control_treatment/Task1InstructionsContent.html'

    input_ids_file = os.path.abspath('control_treatment/_input_ids.csv')



class Subsession(BaseSubsession):
    def creating_session(self):
        # Read IDs
        with open(Constants.input_ids_file, 'r') as f:
            ids = f.read().splitlines()

        random.shuffle(ids)

        for p in self.get_players():
            p.t1_partner_id = ids.pop()


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # Task 1
    t1_c1_1 = models.IntegerField()
    t1_c1_2 = models.IntegerField()
    t1_c1_wrong = models.IntegerField(initial=0)
    t1_c2_1 = models.IntegerField()
    t1_c2_2 = models.IntegerField()
    t1_c2_wrong = models.IntegerField(initial=0)

    t1_partner_id = models.StringField()
    t1_partner_payoff = models.CurrencyField()     # How much the partner will receive
    t1_option = models.IntegerField(            # Option chosen
        choices=[
            [1, 'Option 1'],
            [2, 'Option 2']
        ],
        widget=widgets.RadioSelect
    )

    def set_payoff(self):
        if self.t1_option == 1:
            self.payoff = c(10)
            self. t1_partner_payoff = c(10)
        else:
            self.payoff = c(12)
            self. t1_partner_payoff = c(2)