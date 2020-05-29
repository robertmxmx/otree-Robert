from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random


class Constants(BaseConstants):
    name_in_url = 'task4'
    players_per_group = 2
    num_rounds = 1

    s_total = 18          # total number of statements that will be listed initially
    max_conceal = [0, 2, 5, 9, 16]

    instructions_content = 't3/InstructionsContent.html'
    t1u_instructions = 't1u/InstructionsContent.html'
    t1t_instructions = 't1t/InstructionsContent.html'
    choice_arr = [i for i in range(1, s_total+1)]
    statement_list = [12, 54, 58, 60, 35, 8, 25, 20, 6, 37, 18, 42, 24, 32, 48, 56, 27, 10]         # chosen statements


class Subsession(BaseSubsession):

    def creating_session(self):
        r1_arr = [p for p in self.get_players() if p.participant.id_in_session % 2 == 1]
        r2_arr = [p for p in self.get_players() if p.participant.id_in_session % 2 == 0]
        r2_arr.append(r2_arr.pop(0))

        if len(r1_arr) == len(r2_arr):self.set_group_matrix([list(a) for a in zip(r1_arr, r2_arr)])


class Group(BaseGroup):
    num_random_conceal = models.IntegerField()

    def set_random_conceal(self):
        self.num_random_conceal = random.choice(Constants.max_conceal)


def get_conceal():
    return models.IntegerField(choices=Constants.choice_arr, blank=True, label="")


class Player(BasePlayer):
    # Comprehension Questions
    c1 = models.BooleanField(widget=widgets.RadioSelect)
    c1_wrong = models.IntegerField(initial=0)
    c2 = models.IntegerField(
        choices=[
            [1, "assign it number 1"],
            [2, "assign it number 18"],
            [3, "not assign any number to it"]
        ],
        widget=widgets.RadioSelect
    )
    c2_wrong = models.IntegerField(initial=0)
    # user entered ranking
    conceal1 = get_conceal()
    conceal2 = get_conceal()
    conceal3 = get_conceal()
    conceal4 = get_conceal()
    conceal5 = get_conceal()
    conceal6 = get_conceal()
    conceal7 = get_conceal()
    conceal8 = get_conceal()
    conceal9 = get_conceal()
    conceal10 = get_conceal()
    conceal11 = get_conceal()
    conceal12 = get_conceal()
    conceal13 = get_conceal()
    conceal14 = get_conceal()
    conceal15 = get_conceal()
    conceal16 = get_conceal()
    conceal17 = get_conceal()
    conceal18 = get_conceal()
    # index in list
    conceal1_abs = models.IntegerField()
    conceal2_abs = models.IntegerField()
    conceal3_abs = models.IntegerField()
    conceal4_abs = models.IntegerField()
    conceal5_abs = models.IntegerField()
    conceal6_abs = models.IntegerField()
    conceal7_abs = models.IntegerField()
    conceal8_abs = models.IntegerField()
    conceal9_abs = models.IntegerField()
    conceal10_abs = models.IntegerField()
    conceal11_abs = models.IntegerField()
    conceal12_abs = models.IntegerField()
    conceal13_abs = models.IntegerField()
    conceal14_abs = models.IntegerField()
    conceal15_abs = models.IntegerField()
    conceal16_abs = models.IntegerField()
    conceal17_abs = models.IntegerField()
    conceal18_abs = models.IntegerField()

    num_chosen = models.IntegerField(initial=0)
    actually_concealed = models.IntegerField(initial=0)

    def set_revealed(self):
        s_rankings = [
            self.conceal1, self.conceal2, self.conceal3, self.conceal4, self.conceal5, self.conceal6,
            self.conceal7, self.conceal8, self.conceal9, self.conceal10, self.conceal11, self.conceal12,
            self.conceal13, self.conceal14, self.conceal15, self.conceal16, self.conceal17, self.conceal18
        ]

        s_subset = self.participant.vars['s_subset'].copy()
        to_reveal = []                  # stores statements to reveal
        to_conceal = []                 # stores all statements that were concealed

        for i in range(Constants.s_total):
            ranking = s_rankings[i]
            statement = s_subset[i]['item']

            if ranking is None or ranking == 0:     # reveal all un-ranked statements
                to_reveal.append(statement)
            else:
                self.num_chosen += 1                            # count the number of statements ranked
                if ranking <= self.group.num_random_conceal:
                    self.actually_concealed += 1
                    to_conceal.append(statement)
                else:
                    to_reveal.append(statement)

        self.participant.vars['s_revealed'] = to_reveal.copy()
        self.print_statements(s_subset)

    def print_statements(self, s_subset):
        self.conceal1_abs = s_subset[0]['index']
        self.conceal2_abs = s_subset[1]['index']
        self.conceal3_abs = s_subset[2]['index']
        self.conceal4_abs = s_subset[3]['index']
        self.conceal5_abs = s_subset[4]['index']
        self.conceal6_abs = s_subset[5]['index']
        self.conceal7_abs = s_subset[6]['index']
        self.conceal8_abs = s_subset[7]['index']
        self.conceal9_abs = s_subset[8]['index']
        self.conceal10_abs = s_subset[9]['index']
        self.conceal11_abs = s_subset[10]['index']
        self.conceal12_abs = s_subset[11]['index']
        self.conceal13_abs = s_subset[12]['index']
        self.conceal14_abs = s_subset[13]['index']
        self.conceal15_abs = s_subset[14]['index']
        self.conceal16_abs = s_subset[15]['index']
        self.conceal17_abs = s_subset[16]['index']
        self.conceal18_abs = s_subset[17]['index']
