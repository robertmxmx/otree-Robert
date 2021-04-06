def find_occurrences(players, key_val):
    if len(players) == 0:  # precondition (not really necessary)
        return None

    # store the occurrences. looks like { 'value': 'number_of_times_value_occurred' }
    # for example, if 3 occurred 4 times and 4 occurred 2 times: { 3: 4, 4: 2 }
    occs = {}

    # find occurrences
    for p in players:
        val = p[key_val]
        occs[val] = occs[val] + 1 if val in occs else 1

    # create list of occurrences sorted by most to least occurring
    return occs


def most_common_val(players, key_val, other_val):
    # create list of occurrences sorted by most to least occurring
    occs = find_occurrences(players, key_val)
    occs_list = sorted(occs, key=occs.get, reverse=True)

    # try and prioritise occurrences of values that are not equal to the other_val (either 10 or 3)
    if occs_list[0] == other_val and len(occs_list) > 1:
        most_occ_val = occs_list[1]
    else:
        most_occ_val = occs_list[0]

    # find player that shares most occurring value
    return most_occ_val


def find_based_on_val(players, key_val, val_to_find, excluding, find_equal):
    if len(players) == 0:  # precondition (not really necessary)
        return None

    # find player that has their key_val value equal to val_to_find
    for p in players:
        if p in excluding:
            continue
        if find_equal and p[key_val] == val_to_find:
            return p
        elif not find_equal and p[key_val] != val_to_find:
            return p

    # if val_to_find was not found
    return None