import os

from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
)


DEV_PREFILL = os.environ.get("DEV_PREFILL", "0") == "1"

class Constants(BaseConstants):
    name_in_url = "start"
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    accept = models.BooleanField(
        doc="""Whether subject accepts the consent form""",
        widget=widgets.RadioSelect,
        initial=True if DEV_PREFILL else None,
        choices=[[True, "Accept"], [False, "Reject"]],
    )
