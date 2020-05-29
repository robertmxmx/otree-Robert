from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random


class Constants(BaseConstants):
    name_in_url = 'task1_2'
    players_per_group = None
    num_rounds = 2

    main_instructions = 'task1_2/InstructionsContent.html'
    treatment_instructions = 'task1_2/TreatmentInstructions.html'
    control_instructions = 'task1_2/ControlInstructions.html'


class Subsession(BaseSubsession):
    selected_option = models.IntegerField(initial=random.choice([1, 2]))
    this_task1 = models.BooleanField()

    def creating_session(self):
        self.this_task1 = (self.round_number == 1 and self.session.config['order'] == 1) or (self.round_number == 2 and self.session.config['order'] == 2)


class Group(BaseGroup):

    def set_payoffs(self):
        self.session.vars['task1_selected_option'] = self.subsession.selected_option

        if self.subsession.this_task1:  # task 1
            # get choices of all players
            if self.subsession.selected_option == 1:
                choices = [p.option1 for p in self.get_players()]
            else:
                choices = [p.option2 for p in self.get_players()]

            # get most common choice
            choices_dict = dict((x, choices.count(x)) for x in set(choices))
            most_common_choices = [k for k, v in choices_dict.items() if v == max(choices_dict.values())]

            self.session.vars['most_common_choice'] = most_common_choices

            for p in self.get_players():
                task1_option = p.option1 if self.subsession.selected_option == 1 else p.option2

                if task1_option in most_common_choices:
                    p.payoff += c(10)

                p.participant.vars['task1_option'] = task1_option
                p.participant.vars['task1_payoff'] = p.payoff

        else:   # task 2
            for p in self.get_players():
                p.payoff += c(10)
                p.participant.vars['task2_payoff'] = p.payoff


def create_appropriate_field():
    return models.StringField(
        widget=widgets.RadioSelect,
        choices=["Very socially inappropriate", "Somewhat inappropriate", "Somewhat appropriate",
                 "Very socially appropriate"]
    )


class Player(BasePlayer):
    comp1 = models.StringField(
        widget=widgets.RadioSelect,
        choices=["$0", "$10"]
    )
    comp2 = models.StringField(
        widget=widgets.RadioSelect,
        choices=["$0", "$10"]
    )
    comp1_wrong = models.IntegerField()
    comp2_wrong = models.IntegerField()

    # For treatment comprehension questions
    t_comp1a = models.IntegerField()
    t_comp1b = models.IntegerField()
    t_comp1c = models.IntegerField()
    t_comp2a = models.IntegerField()
    t_comp2b = models.IntegerField()
    t_comp2c = models.IntegerField()
    t_comp3 = models.StringField(
        widget=widgets.RadioSelect,
        choices=["Yes", "No"]
    )
    t_comp1_wrong = models.IntegerField()
    t_comp2_wrong = models.IntegerField()
    t_comp3_wrong = models.IntegerField()

    # For control comprehension questions
    c_comp1a = models.IntegerField()
    c_comp1b = models.IntegerField()
    c_comp2a = models.IntegerField()
    c_comp2b = models.IntegerField()
    c_comp1_wrong = models.IntegerField()
    c_comp2_wrong = models.IntegerField()

    option1 = create_appropriate_field()
    option2 = create_appropriate_field()
