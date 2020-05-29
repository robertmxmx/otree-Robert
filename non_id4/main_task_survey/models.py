from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


class Constants(BaseConstants):
    name_in_url = 'main_task_survey_old'
    players_per_group = None
    num_rounds = 1

    grateful_scale = [[1, 'Not at all grateful'], [2, ''], [3, ''], [4, ''], [5, ''], [6, ''],
                      [7, 'Extremely grateful']]
    angry_scale = [[1, 'Not at all angry'], [2, ''], [3, ''], [4, ''], [5, ''], [6, ''],
                   [7, 'Extremely angry']]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


def create_field(labels):
    return models.IntegerField(
        choices=labels,
        widget=widgets.RadioSelect
    )


class Player(BasePlayer):
    q1a = create_field(Constants.grateful_scale)
    q1b = create_field(Constants.angry_scale)
    q2a = create_field(Constants.grateful_scale)
    q2b = create_field(Constants.angry_scale)
    q3a = create_field(Constants.grateful_scale)
    q3b = create_field(Constants.angry_scale)
