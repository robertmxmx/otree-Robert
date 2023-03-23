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
- If a participant hits "No consent" on the Consent page, bring up a popup that has same text as is currently on the "No Consent page". But this popup should have a "Cancel" button, so that if someone cancels, they can go back and still consent. Idea is to make sure that software is not automatically stuck when someone does not consent, because I might be able to find someone else to take that participant's place. 
- The No Consent page can then be deleted.
- Develop much more rigorous bots that try out multiple combinations of group formation. (Ideally, I'd like to be able to experiment with programming the bots myself -- so have a think about making this code safe for me to tinker with, if possible?) 
- Group sorting bug. The software tends to crash 2 pages after the Initial Survey. I think it is having trouble when there is at least one group which is not sorted by either birth region or political ideology. Only one of the three sessions that completed successfully had an unsorted group. Whereas *all* the sessions that crashed had at least one group like this. 
	- Note that the `sorted_by` variable is empty in unsorted groups, it never contains "no sort" -- is this consistent with what you intended?
	- Relatedly: Would it be a good idea to specify in the variable `sorted_by` a non-empty value if the group is not sorted by either criterion (e.g. "null")?
	- Is it possible that oTree code has been updated after you first wrote the group formation algorithm, and this has broken something?
- Negative payoff bug. Participant `zfpzuxn8` in session `svep3wtq`, received a negative payoff. I think this is because they never got credited with their initial 120 ECU, so after taking their payoff was -100, rather than 20. Investigate and fix.

## Toby To Do

- Fix the videos so that they do not have embedded metadata

## Toby To Review


- Please document in a specific readme for the group reputation 3 app):
	- How to tell whether a given group has a political/birth/no identity
    criterion
	- Explain all variables that relate to payoff
	- **Simon:** Done. Please review
