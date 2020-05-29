from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


class Constants(BaseConstants):
    name_in_url = 'survey'
    players_per_group = None
    num_rounds = 1

    money_ques_labels = ["Strongly Agree", "", "", "", "", "Strongly Disagree"]
    exp_ques2_labels = ["Very likely different", "", "", "", "", "", "Very likely identical"]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


def createMoneyQuestions():
    return models.IntegerField(
        choices=[[i, ""] for i in range(1, len(Constants.money_ques_labels)+1)],
        widget=widgets.RadioSelectHorizontal
    )


class Player(BasePlayer):
    money_q1 = createMoneyQuestions()
    money_q2 = createMoneyQuestions()
    money_q3 = createMoneyQuestions()
    money_q4 = createMoneyQuestions()
    money_q5 = createMoneyQuestions()
    money_q6 = createMoneyQuestions()
    money_q7 = createMoneyQuestions()
    money_q8 = createMoneyQuestions()
    money_q9 = createMoneyQuestions()
    money_q10 = createMoneyQuestions()
    money_q11 = createMoneyQuestions()

    sex = models.StringField(
        choices=[
            'Male',
            'Female',
            'Other'
        ], widget=widgets.RadioSelect)
    age = models.IntegerField(min=0, max=150)
    areaOfStudy = models.StringField(
        choices=[
            'Economics',
            'Marketing',
            'Accounting',
            'Science',
            'Engineering',
            'Humanities',
            'Social Sciences',
            'Other'
        ], widget=widgets.RadioSelect)
    numExperiments = models.IntegerField(min=0)
    religion = models.StringField(
        choices=[
            'Buddhist',
            'Christian',
            'Hindu',
            'Jewish',
            'Muslim',
            'No religion',
            'Other'
        ], widget=widgets.RadioSelect)
    countryOfBirth = models.StringField(initial='')
    yearsInAus = models.IntegerField(min=0)

    exp_ques1 = models.IntegerField(        # 'If you ...'
        choices=[[i, ""] for i in range(1, len(Constants.exp_ques2_labels)+1)],
        widget=widgets.RadioSelectHorizontal
    )



