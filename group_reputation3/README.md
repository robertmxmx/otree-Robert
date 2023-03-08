# Group Reputation 3

## Variables

### Session

- `chosen_task` - Indicates which task is chosen for payment.
- `deterrence` - Toggles the "deterrence" condition which allows A to receive feedback on the outcome of the of Task 1 and includes questions about the the other players regions during the exit survey.
- `online_exp` - Whether a shortened version of the instructions are displayed (`task2\templates\task2\components\instructions\3.html` vs `task2\templates\task2\components\instructions\3shortened.html`)
- `rep_condition` - Toggles the condition that allows player C to know about the membership of the group at the end of Task 2.

### Task 1

- `birth_region` - Participant's birth region. See `_myshared/constants.py` for the list of regions.
- `other_br` - If a participant selects a birth region not from the list, this stores the region they specify instead.
- `pi_q1` to `pi_q7` - Answers to the Political Ideology questions.
- `pi_score` - Sum of `pi_q1` to `pi_q7`. This is needed in the calculation of the above `pol_ideology`.
- `pol_ideology` - The derived political ideology of the player. See `task1\pages.py::FormGroups::after_all_players_arrive` for more information about how this is calculated.
- `rl` - Player's role in the game: A, B or C.
- `sorted_by` - How the group that the player belongs to was sorted by. This can be either by birth region, political ideology or no sort if a suitable sort could not be determined.

### Task 2

- `br` and `pi` - Equivalent to `birth_region` and `pol_ideology` respectively from Task 1.
- `chose_to_take` - Whether the taking player choose to take ECU. The amount taken is defined in `task2\models.py::Constants.take_amount`.
- `comp1_wrong` to `comp5_wrong` - Holds a count of how many times a player answered the related comprehension question incorrectly.
- `comp1` to `comp5` - Answers to comprehension questions.
- `deduct_amount` - The amount that was deducted from the the taking player. This is only taken into account if the taking player choose to take ECU.
- `payoff_after_take` - Player's resulting ECU after the taking player took/did not take ECU.
- `will_spend`, `should_spend` and `same_grouping_should_spend` - Answers to the questions that the "other player" is asked while the taking and deducting player are making their decisions **during Task 1**. A bonus can be earned for `will_spend` and `same_grouping_should_spend`.
- `general_deduction`, `same_grouping_deduction` and `should_spend_guess` - Answers to the questions that the "other player" is asked while the taking and deducting player are making their decisions **during Task 2**. All of these questions have a potential to earn a bonus.
