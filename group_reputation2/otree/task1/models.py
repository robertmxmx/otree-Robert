from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import math, random

from _myshared.constants import REGIONS, LOW_PERC, HIGH_PERC
from _myshared.uploader import get_userdata
from _myshared.output import print_groups
from _myshared.grouping import create_random_groups
from shared import set_reduced_br, create_groups, set_roles


class Constants(BaseConstants):
    name_in_url = 'task1'
    players_per_group = 3
    num_rounds = 1

    choices = [
        [1, "Strongly Agree"],
        [2, "Agree"],
        [3, "Somewhat Agree"],
        [4, "Neither Agree Nor Disagree"],
        [5, "Somewhat Disagree"],
        [6, "Disagree"],
        [7, "Strongly Disagree"]
    ]
    choices_reversed = [
        [7, "Strongly Agree"],
        [6, "Agree"],
        [5, "Somewhat Agree"],
        [4, "Neither Agree Nor Disagree"],
        [3, "Somewhat Disagree"],
        [2, "Disagree"],
        [1, "Strongly Disagree"]
    ]
    regions = REGIONS.copy()
    br_info = {
        'key_val': 'birth_region',
        'num_same_allowed': 2,
        'num_diff_allowed': 1,
        'other_val': len(regions)
    }
    pi_info = {
        'key_val': 'pol_ideology',
        'num_same_allowed': 2,
        'num_diff_allowed': 1,
        'other_val': 2
    }


class Subsession(BaseSubsession):
    def creating_session(self):
        userdata = get_userdata()['rows']

        for idx, p in enumerate(self.get_players()):
            p_data = userdata[idx]
            p.birth_region = p_data['birth_region']
            p.other_br = p_data['other_br']
            p.pi_q1 = p_data['pi_q1']
            p.pi_q2 = p_data['pi_q2']
            p.pi_q3 = p_data['pi_q3']
            p.pi_q4 = p_data['pi_q4']
            p.pi_q5 = p_data['pi_q5']
            p.pi_q6 = p_data['pi_q6']
            p.pi_q7 = p_data['pi_q7']
            p.pay_id = p_data['pay_id']

        br_info = Constants.br_info
        pi_info = Constants.pi_info
        num_per_group = Constants.players_per_group

        # find the political ideology of players
        for p in self.get_players():
            p.set_pi_score()
        scores = [p.pi_score for p in self.get_players()]
        scores.sort()
        # subjects are categorised by political ideology. those with highest scores
        # are coded 1 and those with lowest scores 3, with neutrals as 2.
        # thresholds are defined in /shared.py lines 2 and 3. ideology groups
        # will not be formed based on shared neutral ideology. For example
        # if there are two 2's and one 1 then they will be in the no group
        # condition
        low_per = scores[math.ceil(LOW_PERC * len(scores)) - 1]
        high_per = scores[math.ceil(HIGH_PERC * len(scores)) - 1]
        for p in self.get_players():
            if p.pi_score >= high_per:
                p.pol_ideology = 1
            elif p.pi_score <= low_per:
                p.pol_ideology = 3
            else:
                p.pol_ideology = 2
                
        # setup array
        players = []  # holds players that are still left to sort
        for p in self.get_players():
            players.append({
                'id': p.participant.id_in_session,
                'birth_region': p.birth_region,
                'pol_ideology': p.pol_ideology
            })

        # for the regions that have players with less than Constants.min_br set them to the other type
        players = set_reduced_br(players.copy(), 3, br_info['other_val'])
        random.shuffle(players)

        # sort based on birth region
        new_groups, players = create_groups(players.copy(), br_info, num_per_group)
        final_groups = set_roles(new_groups.copy(), 'birth_region', num_per_group)
        random.shuffle(players)

        # sort based on political ideology
        new_groups, players = create_groups(players.copy(), pi_info, num_per_group)
        final_groups = final_groups + set_roles(new_groups.copy(), 'pol_ideology', num_per_group)
        random.shuffle(players)

        # randomly group the rest
        new_groups = create_random_groups(players.copy(), num_per_group)
        final_groups = final_groups + set_roles(new_groups.copy(), None, num_per_group)

        # set participant data so this shared across apps (tasks)
        for i in range(len(final_groups)):
            for p in final_groups[i]:
                for player in self.get_players():
                    if player.participant.id_in_session == p['id']:
                        player.rl = p['role']
                        player.sorted_by = p['sorted_by']
                        player.participant.vars['group'] = i
                        player.participant.vars['role'] = p['role']
                        player.participant.vars['sorted_by'] = p['sorted_by']
                        player.participant.vars['birth_region'] = p['birth_region']
                        player.participant.vars['pol_ideology'] = p['pol_ideology']

        print_groups(final_groups)

class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pay_id = models.StringField()
    
    birth_region = models.IntegerField(
        label='In what region were you born?',
        choices=[[i+1, Constants.regions[i]] for i in range(len(Constants.regions))],
        widget=widgets.RadioSelect)
    other_br = models.StringField(label='Other region', blank=True)

    pi_q1 = models.IntegerField(label='''
        I don’t like change. There is too great a chance for things to go wrong when things
        change. I prefer it when the same people continue doing what they have always done
        instead of having things change.
    ''', choices=Constants.choices, widget=widgets.RadioSelect)
    pi_q2 = models.IntegerField(label='''
        The environment must be protected for the benefit of mankind and its future even if it
        means that people may have to give up some things or pay more for some things like
        petrol or automobiles.
    ''', choices=Constants.choices_reversed, widget=widgets.RadioSelect)
    pi_q3 = models.IntegerField(label='''
        We should be a nation of many different types of people in order to have the benefit of
        many different points of view even if it means that we have to put up with some people
        and ideas that we don’t like.
    ''', choices=Constants.choices_reversed, widget=widgets.RadioSelect)
    pi_q4 = models.IntegerField(label='''
        The main focus of our lives should be getting a good job so that we can have the money
        we need to get the things we want. After we’ve done that we can worry about what others
        need.
    ''', choices=Constants.choices, widget=widgets.RadioSelect)
    pi_q5 = models.IntegerField(label='''
        There is so much information in newspapers and on the TV that it is hard to know what
        is true. The government should have the authority to approve or disapprove what kind of
        information is put before the public.
    ''', choices=Constants.choices, widget=widgets.RadioSelect)
    pi_q6 = models.IntegerField(label='''
        Sometimes a person gets himself into trouble or makes a bad decision that hurts
        himself or even others. The society should do all it can to assist that person so that he can
        have the opportunity to change and better himself.
    ''', choices=Constants.choices_reversed, widget=widgets.RadioSelect)
    pi_q7 = models.IntegerField(label='''
        I believe that it is a woman’s right to decide for herself whether or not she should have
        an abortion. The government should not be able to tell anyone how to behave in their
        private lives.
    ''', choices=Constants.choices_reversed, widget=widgets.RadioSelect)

    pol_ideology = models.IntegerField()
    pi_score = models.IntegerField()
    rl = models.StringField()
    sorted_by = models.StringField()

    def set_pi_score(self):
        self.pi_score = sum([self.pi_q1, self.pi_q2, self.pi_q3, self.pi_q4, self.pi_q5, self.pi_q6, self.pi_q7])