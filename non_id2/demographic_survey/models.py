from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


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
        choices=[
            'Male',
            'Female',
            'Other',
            'Prefer not to say'
        ],
        widget=widgets.RadioSelectHorizontal
    )
    q2 = models.StringField(
        choices=[
            'Nothing',
            'Law',
            'Political Science',
            'Economics',
            'Accounting',
            'Marketing',
            'Mathematics',
            'Computer Science',
            'Psychology',
            'Medicine',
            'Natural Sciences',
            'Languages',
            'Philosophy',
            'Other'
        ],
        widget=widgets.RadioSelectHorizontal
    )
    q3 = models.StringField()
    q4 = models.IntegerField(min=0, max=100)
    q5 = models.StringField(
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
    q6 = models.StringField(
        choices=[
            '0',
            '1-2',
            '3-6',
            '7-12',
            'more than 12'
        ],
        widget=widgets.RadioSelectHorizontal
    )
