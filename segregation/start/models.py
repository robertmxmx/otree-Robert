from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


class Constants(BaseConstants):
    name_in_url = 'start'
    players_per_group = None
    num_rounds = 1

    temp_dict = {'c1': 2, 'c2': 3, 'c3': 4, 'c4': 3, 'c5': 3}
    correct_vals_noPun = temp_dict.copy()

    temp_dict.update({'c6a': 15, 'c6b': 5})
    correct_vals_pun = temp_dict


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    c1 = models.IntegerField(
        choices=[
            [1, "0 points"],
            [2, "50 points"],
            [3, "150 points"],
            [4, "600 points"]
        ],
        widget=widgets.RadioSelect
    )
    c2 = models.IntegerField(
        choices=[
            [1, "0 points"],
            [2, "50 points"],
            [3, "150 points"],
            [4, "600 points"]
        ],
        widget=widgets.RadioSelect
    )
    c3 = models.IntegerField(
        choices=[
            [1, "90 points"],
            [2, "107 points"],
            [3, "117 points"],
            [4, "125 points"]
        ],
        widget=widgets.RadioSelect
    )
    c4 = models.IntegerField(
        choices=[
            [1, "Try to reside in a town with more Blue residents"],
            [2, "Try to reside in a town with fewer Red residents"],
            [3, "Both of the above"],
            [4, "Neither of the above"]
        ],
        widget=widgets.RadioSelect
    )
    c5 = models.IntegerField(
        choices=[
            [1, "Try to reside in a town with more Blue residents"],
            [2, "Try to reside in a town with fewer Red residents"],
            [3, "Both of the above"],
            [4, "Neither of the above"]
        ],
        widget=widgets.RadioSelect
    )
    c6a = models.IntegerField()
    c6b = models.IntegerField()
