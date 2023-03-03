import random

from _myshared.helpers import find_occurrences, most_common_val, find_based_on_val


def set_roles(groups, key_val, players_per_group):
    if len(groups) == 0:
        return []
    roles = [chr(i) for i in range(ord("A"), ord("A") + players_per_group)]
    if key_val is None:
        for g in groups:
            roles_left = roles.copy()
            for p in g:
                random.shuffle(roles_left)
                p["role"] = roles_left.pop()
                p["sorted_by"] = None
    else:
        for g in groups:
            roles_left = roles.copy()
            occs = find_occurrences(g, key_val)
            most_occuring_val = sorted(occs, key=occs.get, reverse=True)[0]
            for p in g:
                if p[key_val] != most_occuring_val:
                    p["role"] = roles_left.pop(0)
            for p in g:
                if p[key_val] == most_occuring_val:
                    random.shuffle(roles_left)
                    p["role"] = roles_left.pop()
                p["sorted_by"] = key_val
    return groups


def set_reduced_br(players, min_br, other_br):
    occs = find_occurrences(players, "birth_region")

    for p in players:
        if occs[p["birth_region"]] < min_br:
            p["birth_region"] = other_br

    return players


def add_to_group(players, key_val, other_val, excluding, limit, find_equal):
    checked = []  # players already checked for suitability

    # the current player being checked
    current_p = find_based_on_val(players, key_val, other_val, excluding, find_equal)

    # keep adding while there are suitable players
    while current_p is not None:
        checked.append(current_p)
        current_p = find_based_on_val(
            players, key_val, other_val, checked + excluding, find_equal
        )

    # return only the allowed number of players (given by limit)
    return checked[:limit]


def create_groups(players, key_info, players_per_group):
    key_val = key_info["key_val"]
    num_same_allowed = key_info["num_same_allowed"]
    num_diff_allowed = key_info["num_diff_allowed"]
    other_val = key_info["other_val"]
    new_groups = []
    new_players = []
    done = False

    # keep creating while there are unsorted players remaining
    while not done:
        if len(players) == 0:
            new_players = []
            break

        # find player with most commonly occurring value
        current_val = most_common_val(players, key_val, other_val)

        # find players with same birth region or political ideology
        same_to_add = add_to_group(
            players, key_val, current_val, [], num_same_allowed, True
        )
        current_group = same_to_add.copy()

        num_diff = 0
        if current_val != other_val:
            # find players with other as their birth region or political ideology
            other_to_add = add_to_group(
                players, key_val, other_val, current_group, num_diff_allowed, True
            )
            num_diff = len(other_to_add)
            current_group = current_group + other_to_add.copy()

        # find players with different birth region or political ideology
        leftover_to_add = add_to_group(
            players,
            key_val,
            current_val,
            current_group,
            num_diff_allowed - num_diff,
            False,
        )
        current_group = current_group + leftover_to_add.copy()

        # check if valid final group
        if len(current_group) == players_per_group:
            new_groups.append(current_group)
            players = [p for p in players if p not in current_group]
        else:
            done = True
            new_players = players.copy()

    return new_groups, new_players
