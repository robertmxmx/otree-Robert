"""
This file stores code that can be shared across apps
"""


# variables/constants
# the number of rounds in the MAIN task
num_rounds = 12      # todo: change to 12
# the round when the expectation survey will appear
exp_round_num = 1   # todo: change?
# the round that the special round is active
sp_round_num = 11    # todo: change to 11
# whether browser bots are active
bots_on = False     # todo: change to false


# functions
def format_list(li, end_text):
    '''
    Formats a string with commas between elements
    and 'or'/'and' between last 2 elements (or any other text)
    :param  li: list of elements
            end_text: text between last 2 elements
    :return: string in format of: 'li[0], li[1], ...'
    '''

    if len(li) == 0:
        return ""

    string = str(li[0])
    for elem in li[1:-1]:
        string += ", %s" % elem
    if len(li) > 1:
        string += " %s %s" % (end_text, li[-1])
    return string
