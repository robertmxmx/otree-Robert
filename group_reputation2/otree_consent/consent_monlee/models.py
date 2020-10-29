from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

doc = """
Online Consent Form
By: rabsjp
"""

class Constants(BaseConstants):
    name_in_url = 'consent_monlee'
    players_per_group = None
    num_rounds = 1

    # Player's reward for the lowest claim"""
class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass 

class Player(BasePlayer):
    name = models.CharField()
    
    accept = models.BooleanField(
        doc="""Whether subject accepts the consent form""",
        widget=widgets.RadioSelect,
        choices=[
            [True, 'Accept'],
            [False, 'Reject'],
        ])