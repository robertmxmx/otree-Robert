from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


class Constants(BaseConstants):
    name_in_url = 'main_task'
    players_per_group = None
    num_rounds = 1

    comp_answers = {
        "comp1a": 12, "comp1b": 2, "comp1c": 0,
        "comp2a": 10, "comp2b": 10, "comp2c": 0,
        "comp3": False
    }


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # Comprehension questions
    comp1a = models.IntegerField()
    comp1b = models.IntegerField()
    comp1c = models.IntegerField()
    comp2a = models.IntegerField()
    comp2b = models.IntegerField()
    comp2c = models.IntegerField()
    comp3 = models.BooleanField(label='''If you choose Option A or B, then will Participant B ever be informed about 
        this experiment?''', widget=widgets.RadioSelectHorizontal)
    # These are used to count how many times a comprehension question was
    # answered incorrectly
    comp1_wrong = models.IntegerField(initial=0)
    comp2_wrong = models.IntegerField(initial=0)
    comp3_wrong = models.IntegerField(initial=0)
    # Main variables
    option = models.IntegerField()
    payoffA = models.CurrencyField()
    payoffB = models.CurrencyField()

    def set_payoffs(self):
        # sets payoff for player, participant A and participant B
        if self.option == 1:
            self.payoff = c(10)
            self.payoffA = c(10)
            self.payoffB = c(0)
        elif self.option == 2:
            self.payoff = c(12)
            self.payoffA = c(2)
            self.payoffB = c(0)
