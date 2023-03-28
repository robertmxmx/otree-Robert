# Instructions

1. Install [Docker](https://www.docker.com/products/docker-desktop)
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

### Notes

- Update the environment variables through the AWS configuration options
  (go to environment page > Configuration > Edit 'Software' > Environment
  properties). Alternatively, use `eb` to set environment variables:
  ```
  eb setenv OTREE_PRODUCTION=1 ...
  ```

- To reduce costs, first go to environment page > Configuration > Edit
  'Rolling updates and deployments' > Set deployment policy to 'Immutable'.
  Next go back to Configuration > Edit 'Capacity' > Set 'Environment type'
  to 'Single Instance'

- [Cleaning up a deployment](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/GettingStarted.Cleanup.html)

# Group Reputation 3

## Simon To Do

## Toby To Do

- Fix the videos so that they do not have embedded metadata

## Toby To Review

- Please document in a specific readme for the group reputation 3 app):
	- How to tell whether a given group has a political/birth/no identity
    criterion
	- Explain all variables that relate to payoff
	- **Simon: Done. Please review**

- Comprehension question 3, please change the answers to the following:
	(a) Yes, A will learn, regardless of whether A takes from B in Task 1.
	(b) Yes, A will learn, provided A takes from B in Task 1.
	(c) No, A will not learn how B reacted in Task 1.
	The correct answer is (a) in the Deterrence treatment, and (c) in the
  NoDeterrence treatment.
  - **Simon: Done**

- Update the Belief questions. See emailed Word document. Just need to add
  headers to break up the questions. Make sure headings are reasonably large
  and prominent, compared to default text.
  - **Simon: Done**

- If a participant hits "No consent" on the Consent page, bring up a popup
that has same text as is currently on the "No Consent page". But this popup
should have a "Cancel" button, so that if someone cancels, they can go back
and still consent. Idea is to make sure that software is not automatically
stuck when someone does not consent, because I might be able to find someone
else to take that participant's place. 
  - **Simon: Done. I have had to update the field so that it shows as 2
    buttons instead of the Radio Fields**

- The No Consent page can then be deleted.
  - **Simon: Done**

- Negative payoff bug. Participant `zfpzuxn8` in session `svep3wtq`, received
  a negative payoff. I think this is because they never got credited with their
  initial 120 ECU, so after taking their payoff was -100, rather than 20.
  Investigate and fix.
  - **Simon: Fixed. You are right, they never got credited. There was a timing
    issue here that I've fixed so this should not happen again.**

- Group sorting bug. The software tends to crash 2 pages after the Initial
  Survey. I think it is having trouble when there is at least one group which
  is not sorted by either birth region or political ideology. Only one of the
  three sessions that completed successfully had an unsorted group. Whereas
  *all* the sessions that crashed had at least one group like this. 
  - **Simon: I haven't been able to fully track down this bug. I took your
    advice (good thinking by the way!) and downloaded the logs from the
    instance. It was complaining about the database so I've switched over
    to a more powerful and production suitable database engine. I'm hoping
    this will fix it.**
  - Note that the `sorted_by` variable is empty in unsorted groups, it never
    contains "no sort" -- is this consistent with what you intended?
    - **Simon: Yes it is, but I've changed this. See below**
  - Relatedly: Would it be a good idea to specify in the variable `sorted_by`
    a non-empty value if the group is not sorted by either criterion (e.g.
    "null")?
    - **Simon: Good idea. I've changed the value to "none"**
  - Is it possible that oTree code has been updated after you first wrote the
    group formation algorithm, and this has broken something?
    - **Simon: I think this is unlikely. oTree has changed their code, but
      they are good at ensuring that current code bases are backwards
      compatible. As mentioned above, I've updated the database and have
      tested it out with different group formations and larger numbers of
      participants (around 9-15). So far so good, but the more testing the
      better.**

- Develop much more rigorous bots that try out multiple combinations of group
  formation. (Ideally, I'd like to be able to experiment with programming the
  bots myself -- so have a think about making this code safe for me to tinker
  with, if possible?) 
  - **Simon: Unfortunately, due to the fact that data is shared across the
    whole experiment (expecially group formation), creating bots that test
    multiple combinations is not straighforward (if at all possible). I've
    rewritten the tests and hopefully this makes it easier for you to play
    with.**
