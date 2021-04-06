import random, math

from shared import set_reduced_br, create_groups, set_roles
from constants import BR_INFO, PI_INFO, NUM_PER_GROUP
from _myshared.constants import REGIONS
from _myshared.grouping import create_random_groups
from _myshared.output import print_groups
from helpers import parsecsv, printxyz

def main():
    regions = REGIONS.copy()
    batches = parsecsv('in.csv')

    for players in batches:
        valid_players = []

        # For the regions that have number of players that are less than BR_THRESHOLD, 
        # set them to the other type
        BR_THRESHOLD = 3
        players = set_reduced_br(players.copy(), BR_THRESHOLD, BR_INFO['other_val'])
        random.shuffle(players)

        # sort based on birth region
        new_groups, players = create_groups(players.copy(), BR_INFO, NUM_PER_GROUP)
        final_groups = set_roles(new_groups.copy(), 'birth_region', NUM_PER_GROUP)
        random.shuffle(players)

        # sort based on political ideology
        new_groups, players = create_groups(players.copy(), PI_INFO, NUM_PER_GROUP)
        final_groups = final_groups + set_roles(new_groups.copy(), 'pol_ideology', NUM_PER_GROUP)
        random.shuffle(players)

        # randomly group the rest
        new_groups = create_random_groups(players.copy(), NUM_PER_GROUP)
        final_groups = final_groups + set_roles(new_groups.copy(), None, NUM_PER_GROUP)

        # print_groups(final_groups)
        printxyz(final_groups)

if __name__ == '__main__':
    main()