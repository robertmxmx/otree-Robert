from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'survey'
    players_per_group = None
    num_rounds = 1

    labels = ["Very likely different", "", "", "", "", "", "Very likely identical"]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass

def createOpinionQuestions():
    return models.IntegerField(
        choices=[[1,""],[2,""],[3,""],[4,""],[5,""],[6,""],[7,""]],
        widget=widgets.RadioSelectHorizontal
    )

class Player(BasePlayer):

    sex = models.StringField(
        choices = [
            'Male',
            'Female',
            'Other'
        ], widget=widgets.RadioSelect)
    age = models.IntegerField(min=0, max=150)
    areaOfStudy = models.StringField(
        choices = [
            'Economics',
            'Science',
            'Engineering',
            'Humanities',
            'Social Sciences',
            'Other'
        ], widget=widgets.RadioSelect)
    numExperiments = models.IntegerField(min=0)
    religion = models.StringField(
        choices = [
            'Buddhist',
            'Christian',
            'Hindu',
            'Jewish',
            'Muslim',
            'No religion',
            'Other'
        ], widget=widgets.RadioSelect)
    country = models.StringField(initial='')

    exp_ques1 = models.IntegerField(
        choices=[[1,""],[2,""],[3,""],[4,""],[5,""],[6,""],[7,""]],
        widget=widgets.RadioSelectHorizontal
    )
    exp_ques2 = models.LongStringField()
    exp_ques3 = models.LongStringField()


