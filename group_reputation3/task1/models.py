import os

from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
)

from _myshared.constants import REGIONS

DEV_PREFILL = os.environ.get("DEV_PREFILL", "0") == "1"


class Constants(BaseConstants):
    name_in_url = "task1"
    players_per_group = 3
    num_rounds = 1

    survey_bonus = 3.00

    choices = [
        [1, "Strongly Agree"],
        [2, "Agree"],
        [3, "Somewhat Agree"],
        [4, "Neither Agree Nor Disagree"],
        [5, "Somewhat Disagree"],
        [6, "Disagree"],
        [7, "Strongly Disagree"],
    ]
    choices_reversed = [
        [7, "Strongly Agree"],
        [6, "Agree"],
        [5, "Somewhat Agree"],
        [4, "Neither Agree Nor Disagree"],
        [3, "Somewhat Disagree"],
        [2, "Disagree"],
        [1, "Strongly Disagree"],
    ]
    regions = REGIONS.copy()
    br_info = {
        "key_val": "birth_region",
        "num_same_allowed": 2,
        "num_diff_allowed": 1,
        "other_val": len(regions),
    }
    pi_info = {
        "key_val": "pol_ideology",
        "num_same_allowed": 2,
        "num_diff_allowed": 1,
        "other_val": 2,
    }


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


def make_pi(label, reversed=False):
    return models.IntegerField(
        label=label,
        choices=Constants.choices_reversed if reversed else Constants.choices,
        initial=1 if DEV_PREFILL else None,
        widget=widgets.RadioSelect,
    )


class Player(BasePlayer):
    birth_region = models.IntegerField(
        label="In what region were you born?",
        choices=[[i + 1, Constants.regions[i]] for i in range(len(Constants.regions))],
        initial=1 if DEV_PREFILL else None,
        widget=widgets.RadioSelect,
    )
    other_br = models.StringField(label="Other region", blank=True)

    pi_q1 = make_pi(
        """
        I don't like change. There is too great a chance for things to go
        wrong when things change. I prefer it when the same people continue
        doing what they have always done instead of having things change.
        """
    )
    pi_q2 = make_pi(
        """
        The environment must be protected for the benefit of mankind and its
        future even if it means that people may have to give up some things
        or pay more for some things like petrol or automobiles.
        """,
        reversed=True,
    )
    pi_q3 = make_pi(
        """
        We should be a nation of many different types of people in order to
        have the benefit of many different points of view even if it means
        that we have to put up with some people and ideas that we don't
        like.
        """,
        reversed=True,
    )
    pi_q4 = make_pi(
        """
        The main focus of our lives should be getting a good job so that we
        can have the money we need to get the things we want. After we've
        done that we can worry about what others need.
        """
    )
    pi_q5 = make_pi(
        """
        There is so much information in newspapers and on the TV that it is
        hard to know what is true. The government should have the authority
        to approve or disapprove what kind of information is put before the
        public.
        """
    )
    pi_q6 = make_pi(
        """
        Sometimes a person gets himself into trouble or makes a bad decision
        that hurts himself or even others. The society should do all it can
        to assist that person so that he can have the opportunity to change
        and better himself.
        """,
        reversed=True,
    )
    pi_q7 = make_pi(
        """
        I believe that it is a woman's right to decide for herself whether
        or not she should have an abortion. The government should not be
        able to tell anyone how to behave in their private lives.
        """,
        reversed=True,
    )

    pol_ideology = models.IntegerField()
    pi_score = models.IntegerField()
    rl = models.StringField()
    sorted_by = models.StringField()

    def set_pi_score(self):
        self.pi_score = sum(
            [
                self.pi_q1,
                self.pi_q2,
                self.pi_q3,
                self.pi_q4,
                self.pi_q5,
                self.pi_q6,
                self.pi_q7,
            ]
        )
