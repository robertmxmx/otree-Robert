# Instructions

1. Install Docker: https://www.docker.com/products/docker-desktop
2. In **.env** edit the *APP* variable to the name of the app you want to run.
   For example, if you want to run **non_id5** do:
   ```
   APP=non_id5
   ```
3. In this folder, run the below in a terminal
   ```
   chmod +x ./run.sh
   ./run.sh prod
   ```
4. The app runs at http://localhost:8000 and the login credentials are:
	- Username: **admin**
	- Password: **otreee**

## Deploy

1. Change `APP` argument in `Dockerfile` to app that is to be deployed
2. For:
   - New deployment
     ```
     eb init -i
     eb create
     eb open
     ```
   - Current deployment
     ```
     eb deploy
     ```
3. Update the environment variables through the AWS configuration options
   (go to environment page > Configuration > Edit 'Software' > Environment
   properties). The variables for production can be found in `.prod.env`.
   Alternatively, use `eb` to set environment variables:
   ```
   eb setenv OTREE_PRODUCTION=1 ...
   ```

### Notes

- To reduce costs, first go to environment page > Configuration > Edit
  'Rolling updates and deployments' > Set deployment policy to 'Immutable'.
  Next go back to Configuration > Edit 'Capacity' > Set 'Environment type'
  to 'Single Instance'
- To clean up a deployment see [this page](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/GettingStarted.Cleanup.html)

# Group Reputation 3

## Simon To Do

- Bug

````
  File "/usr/local/lib/python3.11/site-packages/otree/models/subsession.py", line 175, in _gbat_try_to_make_new_group
    players_for_group = func(self, waiting_players)
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/app/task2/models.py", line 56, in group_by_arrival_time_method
    group_num = waiting_players[0].participant.vars["group"]
                ~~~~~~~~~~~~~~~^^^
IndexError: list index out of range
INFO:     172.17.0.1:62592 - "POST /p/cd5jvq37/task2/Feedback/20 HTTP/1.1" 302 Found
INFO:     172.17.0.1:62592 - "GET /p/cd5jvq37/task2/Setup/22 HTTP/1.1" 200 OK
INFO:     172.17.0.1:62592 - "POST /p/x3ot5me0/task2/Feedback/20 HTTP/1.1" 302 Found
INFO:     172.17.0.1:62592 - "GET /p/x3ot5me0/task2/Setup/22 HTTP/1.1" 200 OK
````
This occurred when running a session with 9 participants, two groups were formed on birth region, one formed on political ideology. Reputation and Deterrence treatments both active. We had just finished the feedback for Task 1 when the error kicked in.

- Det/Rep -- make sure you have tested all four combinations of these config variables.
- Line 41 in FeedbackResults.html, I've put in a line saying how much A would have had deducted. But can you please amend this to say:

	> 	   This would have led to A earning 120 - {{ results.amount_reduced }} = X ECU.

	Where X updates with the correct amount.

- For all the belief questions, remove the calculate buttons
- Belief questions: the belief questions that should be shown in REP treatment, were not shown to the group based on political values (for all of A, B, and C). Is that because there was only *one* political group?
- As well as groups formed on the basis of birth region, there are groups
  formed on the basis of political ideology. And there are groups formed on
  the basis of no identity criterion. If the *latter*, they should not receive
  questions that make reference to "some group criterion". But if political ideology, they still should receive those questions.

## Toby To Do

- Confirm that nothing funny happens if a group is not based on any identity
  criterion

## Toby To Review

- Important change to feedback for A: A needs to learn how **B/C would have
  behaved, even if A does not take**. (In both Task 1 and Task 2.) TOBY to
  add change to the wording, but leave the logic to be filled in by Simon.
  - **Simon:** I've tried to clean up the code here. If you want to add the
    wording you will need to edit this file:
    `group_reputation3/task2/templates/components/FeedbackResults.html`
		- Toby: I've tried to add feedback. 
- Update readme to describe new variables correctly
- Head the belief questions page "Bonus questions"
- On the final payment page, refer to the bonus payment as "Bonus question
  payment" (if applicable). (Toby to check)
- Yes, "chosen" task, for all participants as config variable, affects whether
  Task 1 or Task 2 is paid BUT for bonus question: 
  - Everyone gets the chance to earn a bonus from belief questions.
  - Randomize separately for each participant which belief question is to be
    rewarded. Store the name of the variable which is the basis of the bonus
    for each individual. Give them feedback about exactly which question it was
    that they are getting a bonus for on the payoff page.
- Implement new belief questions (refinement of questions for B and C, new
  questions for A)
  - **Simon:** Done. You can find the questions in
    `group_reputation3/task2/templates/components/belief_questions`
- Please document in a specific readme for the group reputation 3 app):
	- How to tell whether a given group has a political/birth/no identity
    criterion
	- Explain all variables that relate to payoff
	- **Simon:** Done. Please review
- The waiting task questions need to be revised. Basic idea is as follows
  ```
  Ask C:
    - How much *will* B punish? (incentivized)
    - How much is *appropriate* to punish? (not incentivized) 
    - What do you predict is the most common answer to this question among
      people with same group identity?
  Ask B: 
    - How much did B's in general punish? (most common, incentivized)
    - How much did other B's from your birth region/political orientation
      punish? (most common, incentivized)
    - What is most common answer by C's from your birth region to question "how
      much is appropriate for B to punish?" (incentivized)
  ```
	- **Simon:** Done. A few things to note: 
		- I've made the wording "politically conservative/progressive" where
      players that are in the high percentile are considered progressive and
      those in the low percentile are conservative. Is this correct? 
		- As part of this change, I've removed the "will_spend_guess" variable
      since it's no longer being used.
		- The last question for C and the last 2 questions for B should only
      appear if there are other groups that are sorted the same, is that right?
- Participant C earned no bonus, but on C's payment info page it reports "Task
  1 bonus: $0.00" (see pic) -- this information should only appear on a
  participant's page if they earned a bonus.
    - Hide your payment info *is* required. Please add it back.
    - **Simon:** Done. While making this change I noticed that "Click here to
      hide your payment info" was added to the payment info page. I assume
      this isn't needed/used so I removed it.
- "Internet requirements to participate" page: remove this page, unless "online
  option" is chosen in config.
- Identify bug in Task 2 feedback page. In TH's test, B's endowment went up by
  20, but B's endowment cannot change in Task 2. I suspect the feedback page is
  reflecting that B earned a bonus in Task 1. But bonus payments should NEVER
  be shown on the feedback page at end of each round. They are only shown to
  individual players at end of experiment.
    - **Simon:** Done. Please test to make sure.
- TH: I can't see why Player B earned a bonus in my test run (see data
  provided). In Task 2, Player B guessed C woud spend 4, and said C **should
  spend** 3. C actually spend 7. Bonus should only be paid if what C spends
  what B says C *will* spend.
    - **Simon:** This bonus comes from B correctly guessing C's answers in
      Task 1. In Task 1 C said that B will spend 4 ECU (will_spend) and said
      that B should spend 3 ECU (should_spend), then in Task 2, B correctly
      guessed the amounts of will_spend and should_spend so they got 2 (1 for
      each guess) * 10 = 20 ECU as a bonus.
- TH: Also: I think we previously had it that you could earn a bonus on either
  task. Let's change it so you only get the bonus if you make a correct guess
  **on the task that is chosen for payment**. I've tweaked the wording of the
  relevant page, but you'll need to change the logic of the payment calculation.
    - **Simon:** Done. New session variable called **chosen_task** which picks
      the task that is chosen for payment.
