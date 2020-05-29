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
    max_conceal = [0, 2, 6, 12, 16, 18]

    instructions_content = 'task4/InstructionsContent.html'
    choice_arr = [i for i in range(1, s_total+1)]
    statement_list = [12, 54, 58, 60, 35, 8, 25, 20, 6, 37, 18, 42, 24, 32, 48, 56, 27, 10]         # chosen statements

    list_of_statements_file = 't4_list_of_statements.txt'


class Subsession(BaseSubsession):

    def creating_session(self):
        r1_arr = [p for p in self.get_players() if p.participant.id_in_session % 2 == 1]
        r2_arr = [p for p in self.get_players() if p.participant.id_in_session % 2 == 0]
        r2_arr.append(r2_arr.pop(0))
        r2_arr.append(r2_arr.pop(0))

        if len(r1_arr) != len(r2_arr):
            print("not even amount of players")
        else:
            self.set_group_matrix([list(a) for a in zip(r1_arr, r2_arr)])

        with open(Constants.list_of_statements_file, 'w') as f:
            f.write("")


class Group(BaseGroup):
    num_random_conceal = models.IntegerField()

    def set_random_conceal(self):
        self.num_random_conceal = random.choice(Constants.max_conceal)


def get_conceal():
    return models.IntegerField(choices=Constants.choice_arr, blank=True, label="")


class Player(BasePlayer):
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
    num_chosen = models.IntegerField()


    def set_revealed(self):
        s_rankings = [self.conceal1, self.conceal2, self.conceal3, self.conceal4, self.conceal5, self.conceal6,
                      self.conceal7, self.conceal8, self.conceal9, self.conceal10, self.conceal11, self.conceal12,
                      self.conceal13, self.conceal14, self.conceal15, self.conceal16, self.conceal17, self.conceal18]

        s_subset = self.participant.vars['s_revealed'].copy()
        to_reveal = []                  # stores statements to reveal
        sp_dict = {}                    # to find the statements (that were ranked) to reveal

        for i in range(Constants.s_total):
            if s_rankings[i] is None or s_rankings[i] == 0:
                to_reveal.append(s_subset[i])
            else:
                sp_dict[i] = s_rankings[i]

        s_list = sorted(sp_dict, key=sp_dict.get)           # sort by ranking
        self.num_chosen = len(s_list)
        num_random_conceal = self.group.num_random_conceal

        if num_random_conceal <= self.num_chosen:
            for i in range(num_random_conceal, self.num_chosen):
                to_reveal.append(s_subset[s_list[i]])

        self.participant.vars['s_revealed'] = to_reveal.copy()