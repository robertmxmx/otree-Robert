def create_random_groups(players, players_per_group):
    # this stores players that haven't been sorted above and so will be put into random groups
    new_groups = []

    # sort leftover players into random groups
    while len(players) != 0:
        current_group = []

        # create groups with num players = players_per_group
        for _ in range(players_per_group):
            current_group.append(players.pop())

        # check if valid final group
        if len(current_group) == players_per_group:
            new_groups.append(current_group)

    return new_groups