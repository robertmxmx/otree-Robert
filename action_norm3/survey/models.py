from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


class Constants(BaseConstants):
    name_in_url = 'survey'
    players_per_group = None
    num_rounds = 1

    label_fair = [[1, 'Not at all fair'], [2, ''], [3, ''], [4, ''], [5, ''], [6, ''], [7, 'Completely fair']]
    label_likely = [[1, 'Not at all likely'], [2, ''], [3, ''], [4, ''], [5, ''], [6, ''], [7, 'Very likely']]
    label_much = [[1, 'Not at all'], [2, ''], [3, ''], [4, ''], [5, ''], [6, ''], [7, 'Very much']]
    label_agree = [[1, 'Strongly disagree'], [2, ''], [3, ''], [4, ''], [5, ''], [6, ''], [7, 'Strongly agree']]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    sex = models.StringField(
        choices=["Male", "Female", "Other"],
        widget=widgets.RadioSelect
    )
    age = models.IntegerField(min=0)
    area_of_study = models.StringField(
        choices=["Economics", "Marketing", "Accounting", "Science", "Engineering", "Humanities", "Social Sciences",
            "Other"],
        widget=widgets.RadioSelect
    )
    area_of_study_other = models.StringField(blank=True)
    num_exps = models.StringField(
        choices=["0", "1-2", "2-3", "4-8", "More than 8"],
        widget=widgets.RadioSelect
    )
    religion = models.StringField(
        choices=["Buddhist", "Christian", "Hindu", "Jewish", "Muslim", "No religion", "Other"],
        widget=widgets.RadioSelect
    )
    religion_other = models.StringField(blank=True)
    birth_country = models.StringField(
        choices=["Malaysia", "Australia", "Singapore", "China", "India", "Bangladesh", "Indonesia", "Other"],
        widget=widgets.RadioSelect
    )
    birth_country_other = models.StringField(blank=True)
    num_years_aus = models.IntegerField(min=0)
    q1 = models.IntegerField(choices=Constants.label_fair, widget=widgets.RadioSelect)
    q2 = models.IntegerField(choices=Constants.label_fair, widget=widgets.RadioSelect)
    q3 = models.IntegerField(choices=Constants.label_likely, widget=widgets.RadioSelect)
    q4 = models.IntegerField(choices=Constants.label_likely, widget=widgets.RadioSelect)
    survey_cause_red1 = models.IntegerField(choices=Constants.label_agree, widget=widgets.RadioSelect)      # for 2r1g
    survey_cause_green1 = models.IntegerField(choices=Constants.label_agree, widget=widgets.RadioSelect)
    survey_cause_red2 = models.IntegerField(choices=Constants.label_agree, widget=widgets.RadioSelect)      # for 1r2g
    survey_cause_green2 = models.IntegerField(choices=Constants.label_agree, widget=widgets.RadioSelect)
    survey_cause_red3 = models.IntegerField(choices=Constants.label_agree, widget=widgets.RadioSelect)      # for 2r2g
    survey_cause_green3 = models.IntegerField(choices=Constants.label_agree, widget=widgets.RadioSelect)
    survey_cause_explain = models.LongStringField(label='''Please write below to explain what you think it means
        for one thing to cause another, and why you answered the way you did to the above questions''')
