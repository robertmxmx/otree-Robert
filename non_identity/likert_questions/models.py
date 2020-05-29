from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'likert_questions'
    players_per_group = None
    num_rounds = 1

    questions_file = '_likert_questions.txt'


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


def get_question():
    with open(Constants.questions_file, 'r') as f:
        for line in f:
            yield models.IntegerField(
                label=line,
                choices=[
                    [1, ' Strongly Disagree'],
                    [2, 'Disagree'],
                    [3, 'Somewhat Disagree'],
                    [4, 'Neither Agree Nor Disagree'],
                    [5, 'Somewhat Agree'],
                    [6, 'Agree'],
                    [7, 'Strongly Agree']
                ],
                widget=widgets.RadioSelect
            )


nextq = get_question()


class Player(BasePlayer):
    q1 = next(nextq)
    q2 = next(nextq)
    q3 = next(nextq)
    q4 = next(nextq)
    q5 = next(nextq)
    q6 = next(nextq)
    q7 = next(nextq)
    q8 = next(nextq)
    q9 = next(nextq)
