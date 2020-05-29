from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'demographic_survey'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    q1 = models.StringField(
        label="I identify as",
        choices=[
            'Male',
            'Female',
            'Other',
            'Prefer not to say'
        ],
        widget=widgets.RadioSelectHorizontal
    )
    q2 = models.StringField(
        label="Major",
        choices=[
            'Nothing',
            'Law/Political Science',
            'Economics',
            'Mathematics/Computer Science',
            'Psychology',
            'Medicine',
            'Natural Sciences',
            'Languages',
            'Philosophy',
            'Other'
        ],
        widget=widgets.RadioSelectHorizontal
    )
    q3 = models.StringField(label="Country I was born in")
    q4 = models.IntegerField(min=0, max=100)
    q5 = models.StringField(
        label="Religious Affiliation",
        choices=[
            'Christianity',
            'Judaism',
            'Islam',
            'Hinduism',
            'Buddhism',
            'Sikhism',
            'Atheism/Agnosticism/Secularism',
            'Other'
        ],
        widget=widgets.RadioSelectHorizontal
    )
    q6 = models.IntegerField(
        label="Number of MonLEE experiments I have participated in",
        min=0
    )
