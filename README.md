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

- To clean up a deployment see
  [this page](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/GettingStarted.Cleanup.html)

# Group Reputation 3

## Simon To Do

- Comprehension question 3, please change the answers to the following:
	a.	Yes, A will learn, regardless of whether A takes from B in Task 1.
	b.	Yes, A will learn, provided A takes from B in Task 1.
	c.	No, A will not learn how B reacted in Task 1.

	The correct answer is (a) in the Deterrence treatment, and (c) in the NoDeterrence treatment.
- Update the Belief questions. See emailed Word document. Just need to add headers to break up the questions. Make sure headings are reasonably large and prominent, compared to default text.

## Toby To Do


## Toby To Review


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
  This occurred when running a session with 9 participants, two groups were
  formed on birth region, one formed on political ideology. Reputation and
  Deterrence treatments both active. We had just finished the feedback for
  Task 1 when the error kicked in.

  No such error occurred in a session with Det treatment switched off.
  - **Simon:** I can't reproduce this error at all. I'm hoping this is a one off.

- Please document in a specific readme for the group reputation 3 app):
	- How to tell whether a given group has a political/birth/no identity
    criterion
	- Explain all variables that relate to payoff
	- **Simon:** Done. Please review
