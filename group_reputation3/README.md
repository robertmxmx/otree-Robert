# Group Reputation 3 Variables

- A `*` in a variable name indicates a number

## Session

| Name          | Description |
| ------------- | ----------- |
| chosen_task   | The task that is chosen for payment |
| deterrence    | Toggles the "deterrence" condition which allows A to receive feedback on the out come of Task 1. This feedback includes questions about the other players regions during the exit survey. |
| online_exp    | Whether a shortened version of the instructions are displayed (`3.html` vs `3shortened.html`) |
| rep_condition | Toggles the condition that allows player C to know about the membership of the group at the end of Task 2. |

## Task 1

| Name          | Description |
| ------------- | ----------- |
| birth_region | Participant's birth region. See `_myshared/constants.py` for the list of regions. |
| other_br     | If a participant selects a birth region not from the list, this stores the region they specify instead |
| pi_q*        | Answers to the Political Ideology questions |
| pi_score     | Sum of `pi_q1` to `pi_q7`. This is needed in the calculation of `pol_ideology`. |
| pol_ideology | The derived political ideology of the player. See `task1\pages.py::FormGroups::after_all_players_arrive` for more information about how this is calculated. |
| rl           | Player's role in the game: A, B or C |
| sorted_by    | How the group that the player belongs to was sorted by. This can be either by birth region, political ideology or no sort if a suitable sort could not be determined. |

## Task 2

| Name              | Description |
| ----------------- | ----------- |
| br and pi         | Equivalent to `birth_region` and `pol_ideology` respectively from Task 1. |
| comp*             | Answers to comprehension questions. |
| comp*_wrong       | A count of how many times a player answered the related comprehension question incorrectly. |
| chose_to_take     | Whether the taking player choose to take ECU. The amount taken is defined in `task2\models.py::Constants.take_amount`. |
| deduct_amount     | The amount that was deducted from the the taking player. This is only taken into account if the taking player choose to take ECU. |
| payoff_after_take | Player's resulting ECU after the taking player took/did not take ECU. |
| bonus_q_to_pay    | The randomly chosen bonus question that will be paid if the player answers it correctly. This is random for each player. |
| bonus_paid        | Whether the player answered the bonus question correctly or not |

Below are the Bonus Question variables and the question number that they are
associated with. You can find the full questions in the HTML templates at
`task2/templates/components/belief_questions/`

| Name           | Question Number |
| -------------- | --------------- |
| ee_c_group     | 1               |
| ee_c_session   | 2               |
| ne_c           | 3               |
| ne_c_c_group   | 4               |
| ne_c_c_session | 5               |
| ee_b_group     | 1               |
| ee_b_session   | 2               |
| ne_b           | 3               |
| ne_b_b_group   | 4               |
| ne_b_b_session | 5               |
| ne_b_c_group   | 6               |
| ne_b_c_session | 7               |
| ee_a_group     | 1               |
| ee_a_session   | 2               |
| ne_a           | 3               |
| ne_a_b_group   | 4               |
| ne_a_b_session | 5               |
| ne_a_c_group   | 6               |
| ne_a_c_session | 7               |
