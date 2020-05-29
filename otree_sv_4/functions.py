def shift_groups(initial_groups, shift_by):
    group_matrix = []

    # all odd numbered participants have id_in_group = 1
    for group in initial_groups:
        group_matrix.append([group[0]])
    
    # all even numbered particpants have id_in_group = 2 and have been
    # shuffled over shift_by amount. for example if shift_by=1: 
    # original = [[p1, p2], [p3, p4], [p5, p6]]
    # new      = [[p1, p6], [p3, p2], [p5, p4]] 
    for i in range(len(initial_groups)):
        index = (i-shift_by) % len(initial_groups)
        group_matrix[i].append(initial_groups[index][1])

    return group_matrix