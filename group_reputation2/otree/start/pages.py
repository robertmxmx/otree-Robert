from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

import csv

PLAYER_DATA_FILE = 'player_data.csv'
PLAYER_STRING_ATTRIBUTES = [
    'role',
    'sorted_by',
]
PLAYER_INTEGER_ATTRIBUTES = [
    'group',
    'birth_region',
    'pol_ideology'
]

"""
Get the players information, such as birth region, political
ideology, etc. from a csv file
"""
def get_player_data():
    players = []
    with open(PLAYER_DATA_FILE, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            p_info = {}
            for attr in PLAYER_STRING_ATTRIBUTES:
                p_info[attr] = row[attr]
            for attr in PLAYER_INTEGER_ATTRIBUTES:
                p_info[attr] = int(row[attr])
            players.append(p_info)
    return players

class Main(Page):

    def vars_for_template(self):
        return {
            'aud_per_point': c(1).to_real_world_currency(self.session)
        }

class FormGroups(WaitPage):
    wait_for_all_groups = True

    def after_all_players_arrive(self):
        player_data = get_player_data()
        i = 0

        for player in self.subsession.get_players():
            for attr in PLAYER_STRING_ATTRIBUTES + PLAYER_INTEGER_ATTRIBUTES:
                player.participant.vars[attr] = player_data[i][attr]
            i += 1


page_sequence = [
    Main,
    FormGroups
]
