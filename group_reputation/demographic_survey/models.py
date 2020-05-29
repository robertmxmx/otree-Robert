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


def create_region_field(label):
    return models.IntegerField(
        label=label,
        choices=[
            [1, "Very unlikely (<10%)"],
            [2, "Unlikely (10-30%)"],
            [3, "Some chance (30-50%)"],
            [4, "More likely than not (50%-70%)"],
            [5, "Likely (70-90%)"],
            [6, "Highly likely (>90%)"]
        ],
        widget=widgets.RadioSelect
    )


class Player(BasePlayer):
    area_of_study = models.StringField(
        label="If you are a student, which of the following is your main area of study?",
        choices=[
            'Economics',
            'Engineering',
            'Marketing',
            'Physics',
            'Accounting',
            'Humanities',
            'Social Sciences',
            'Other',
            'Not a student'
        ], widget=widgets.RadioSelect
    )
    supporting_competition = models.IntegerField(
        label="Do you support a football team in one of the following competitions?",
        choices=[
            [1, 'English premier league football'],
            [2, 'Australian rules (AFL)'],
            [3, 'American football (NFL)'],
            [4, 'None']
        ],
        widget=widgets.RadioSelect
     )
    supporting_team = models.StringField(blank=True, label="If yes, who:")
    num_experiments = models.IntegerField(label="How many experiments have you done in MonLEE in the past?")
    gender = models.StringField(
        label="Gender",
        choices=['Male', 'Female', 'Other'],
        widget=widgets.RadioSelectHorizontal
    )
    similarity1 = models.IntegerField(choices=list(range(1, 7+1)), widget=widgets.RadioSelect)
    similarity2 = models.IntegerField(choices=list(range(1, 7+1)), widget=widgets.RadioSelect)
    BC_from_China = create_region_field("China (mainland)")
    BC_from_Malaysia = create_region_field("Malaysia")
    BC_from_Australia = create_region_field("Australia")
    BC_from_Singapore = create_region_field("Singapore")
    BC_from_India = create_region_field("India")
    BC_from_Hong_Kong = create_region_field("Hong Kong")
    A_from_China = create_region_field("China (mainland)")
    A_from_Malaysia = create_region_field("Malaysia")
    A_from_Australia = create_region_field("Australia")
    A_from_Singapore = create_region_field("Singapore")
    A_from_India = create_region_field("India")
    A_from_Hong_Kong = create_region_field("Hong Kong")

    def role(self):
        return self.participant.vars['role']
