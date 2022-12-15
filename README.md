# Instructions

1. Install Docker: https://www.docker.com/products/docker-desktop
1. In **.env** edit the *APP* variable to the name of the app you want to run.
   For example, if you want to run **non_id5** do:
   ```
   APP=non_id5
   ```
1. In this folder, run the below in a terminal
   ```
   chmod +x ./run.sh
   ./run.sh prod
   ```
1. The app runs at http://localhost:8000 and the login credentials are:
	- Username: **admin**
	- Password: **otreee**

## Deploying

1. Change `APP` argument in `Dockerfile` to app that is to be deployed
1. For:
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
1. **IMPORTANT** - Remember to update the environment variables through the AWS
   configuration options (go to environment page > Configuration > Edit
   'Software' > Environment properties). The variables for production can be
   found in `.prod.env`

# Group Reputation 3

## To do

- Participant C earned no bonus, but on C's payment info page it reports "Task 1 bonus: $0.00" (see pic) -- this information should only appear on a participant's page if they earned a bonus.
    - Simon: Done. While making this change I noticed that "Click here to hide your payment info" was added to the payment info page. I assume this isn't needed/used so I removed it.
    	- Hide your payment info *is* required. Please add it back.
- Please document in a specific readme for the group reputation 3 app):
	- how to tell whether a given group has a political/birth/no identity criterion
	- explain all variables that relate to payoff
- The waiting task questions need to be revised. Basic idea is as follows

	Ask C:

	- How much *will* B punish? (incentivized)
	- How much is *appropriate* to punish? (not incentivized) 
	- What do you predict is the most common answer to this question among people with same group identity?

	
	Ask B: 
	
	- How much did B's in general punish? (most common, incentivized)
	- How much did other B's from your birth region/political orientation punish? (most common, incentivized)
	- What is most common answer by C's from your birth region to question "how much is appropriate for B to punish?" (incentivized)
	



## Toby to review

- "Internet requirements to participate" page: remove this page, unless "online option" is chosen in config.
	- Simon: Done
- Identify bug in Task 2 feedback page. In TH's test, B's endowment went up by 20, but B's endowment cannot change in Task 2. I suspect the feedback page is reflecting that B earned a bonus in Task 1. But bonus payments should NEVER be shown on the feedback page at end of each round. They are only shown to individual players at end of experiment.
    - Simon: Done. Please test to make sure.
- TH: I can't see why Player B earned a bonus in my test run (see data provided). In Task 2, Player B guessed C woud spend 4, and said C **should spend** 3. C actually spend 7. Bonus should only be paid if what C spends what B says C *will* spend.
    - Simon: This bonus comes from B correctly guessing C's answers in Task 1. In Task 1 C said that B will spend 4 ECU (will_spend) and said that B should spend 3 ECU (should_spend), then in Task 2, B correctly guessed the amounts of will_spend and should_spend so they got 2 (1 for each guess) * 10 = 20 ECU as a bonus.
- TH: Also: I think we previously had it that you could earn a bonus on either task. Let's change it so you only get the bonus if you make a correct guess **on the task that is chosen for payment**. I've tweaked the wording of the relevant page, but you'll need to change the logic of the payment calculation.
    - Simon: Done. New session variable called **chosen_task** which picks the task that is chosen for payment.
