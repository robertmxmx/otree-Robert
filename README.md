# Instructions

- Install Docker: https://www.docker.com/products/docker-desktop
- In **.env** edit the *APP* variable to the name of the app you want to run. For example, if you want to run **non_id5** do:
```
APP=non_id5
```
- Run:
```
docker compose -f <environment>.yml up --build
```
where `<environment>` is either "development", "staging" or "production"

## Running the app

Also remember that the app runs at http://localhost:8000 and if you need to login the credentials are:

- Username: admin
- Password: otreee

## ToDo - Group reputation 3

- PayID page: remove this page from the experiment
- TH has changed wording of the consent form. Check he hasn't broken it
- Identify bug in Task 2 feedback page. In TH's test, B's endowment went up by 20, but B's endowment cannot change in Task 2. I suspect the feedback page is reflecting that B earned a bonus in Task 1. But bonus payments should NEVER be shown on the feedback page at end of each round. They are only shown to individual players at end of experiment.
- TH: I can't see why Player B earned a bonus in my test run (see data provided). In Task 2, Player B guessed C woud spend 4, and said C **should spend** 3. C actually spend 7. Bonus should only be paid if what C spends what B says C *will* spend.
- TH: Also: I think we previously had it that you could earn a bonus on either task. Let's change it so you only get the bonus if you make a correct guess **on the task that is chosen for payment**. I've tweaked the wording of the relevant page, but you'll need to change the logic of the payment calculation.
- Participant C earned no bonus, but on C's payment info page it reports "Task 1 bonus: $0.00" (see pic) -- this information should only appear on a participant's page if they earned a bonus.