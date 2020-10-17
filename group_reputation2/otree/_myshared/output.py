def print_groups(groups):
    # check that that an empty list isn't being printed
    if len(groups) == 0:
        print("none\n")

    # print to console and file
    headers = ['group', 'player_id', 'role', 'br', 'pi', 'sorted_by']

    for h in headers:
        print('%-15s' % h, end='')

    print('\n' + '-'*90)

    for i in range(len(groups)):
        for p in groups[i]:
            print("%-15d%-15s%-15s%-15s%-15s%-15s" % (
                i+1, 
                p['id'], 
                p['role'], 
                p['birth_region'], 
                p['pol_ideology'], 
                p['sorted_by']
            ))