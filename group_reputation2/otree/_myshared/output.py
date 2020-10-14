def print_groups(groups):
    # check that that an empty list isn't being printed
    if len(groups) == 0:
        print("none\n")

    # print to console and file
    print("group,player_id,role,birth region,political ideology,sorted by")
    for i in range(len(groups)):
        for p in groups[i]:
            print("%d,%s,%s,%s,%s,%s" % (
                i+1, 
                p['id'], 
                p['role'], 
                p['birth_region'], 
                p['pol_ideology'], 
                p['sorted_by']
            ))