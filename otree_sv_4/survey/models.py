from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)


class Constants(BaseConstants):
    name_in_url = 'survey'
    players_per_group = None
    num_rounds = 1

    likert_similar = [
        [1, 'Very much like me'], 
        [2, 'Like me'], 
        [3, 'Somewhat like me'], 
        [4, 'A little like me'], 
        [5, 'Not like me'], 
        [6, 'Not at all like me']
    ]
    likert_different = [
        [1, 'Very likely different'], 
        [2, ''], 
        [3, ''], 
        [4, ''], 
        [5, ''], 
        [6, ''],
        [7, 'Very likely identical']
    ]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    similar1 = models.IntegerField(
        label='''It is important to this person to think up new ideas 
            and be creative; to do things one's own way''',
        choices=Constants.likert_similar,
        widget=widgets.RadioSelect
    )
    similar2 = models.IntegerField(
        label='''It is important to this person to be rich; to have 
            a lot of money and expensive things''',
        choices=Constants.likert_similar,
        widget=widgets.RadioSelect
    )
    similar3 = models.IntegerField(
        label='''Living in secure surroundings is important to this 
            person; to avoid anything that might be dangerous''',
        choices=Constants.likert_similar,
        widget=widgets.RadioSelect
    )
    similar4 = models.IntegerField(
        label='''It is important to this person to have a good
            time; to "spoil" oneself''',
        choices=Constants.likert_similar,
        widget=widgets.RadioSelect
    )
    similar5 = models.IntegerField(
        label='''It is important to this person to do something
            for the good of society''',
        choices=Constants.likert_similar,
        widget=widgets.RadioSelect
    )
    similar6 = models.IntegerField(
        label='''It is important for this people to help the people
            nearby; to care for their well-being''',
        choices=Constants.likert_similar,
        widget=widgets.RadioSelect
    )
    similar7 = models.IntegerField(
        label='''Being very successful is important to this person;
            to have people recognize one's achievements''',
        choices=Constants.likert_similar,
        widget=widgets.RadioSelect
    )
    similar8 = models.IntegerField(
        label='''Adventure and taking risks are important to this
            person; to have an exciting life''',
        choices=Constants.likert_similar,
        widget=widgets.RadioSelect
    )
    similar9 = models.IntegerField(
        label='''It is important to this person to always behave
            properly; to avoid doing anything people would say 
            is wrong''',
        choices=Constants.likert_similar,
        widget=widgets.RadioSelect
    )
    similar10 = models.IntegerField(
        label='''Looking after the environment is important to
            this person; to care for nature and save life 
            resources''',
        choices=Constants.likert_similar,
        widget=widgets.RadioSelect
    )
    similar11 = models.IntegerField(
        label='''Tradition is important to this person, to 
            follow the customs handed down by one's religion
            or family''',
        choices=Constants.likert_similar,
        widget=widgets.RadioSelect
    )
    sex = models.StringField(
        label="Sex",
        choices=["Male", "Female", "Other"],
        widget=widgets.RadioSelectHorizontal
    )
    age = models.IntegerField(label="Age in years", min=0)
    area_of_study = models.StringField(
        label="Area of study",
        choices=[
            "Economics", 
            "Marketing", 
            "Accounting", 
            "Science", 
            "Engineering", 
            "Humanities", 
            "Social Sciences",
            "Other"
        ],
        widget=widgets.RadioSelectHorizontal
    )
    num_exps = models.IntegerField(
        label="Number of experiments completed in MONLEE in the past",
        min=0
    )
    religion = models.StringField(
        label="Religion",
        choices=[
            "Buddhist", 
            "Christian", 
            "Hindu", 
            "Jewish", 
            "Muslim", 
            "No religion", 
            "Other"
        ],
        widget=widgets.RadioSelectHorizontal
    )
    birth_country = models.StringField(
        label="Region of birth",
        choices=[
            "Malaysia", 
            "Australia", 
            "Singapore", 
            "China", 
            "India", 
            "Bangladesh", 
            "Indonesia", 
            "Other:"
        ],
        widget=widgets.RadioSelect
    )
    birth_country_other = models.StringField(
        label="Other",
        blank=True
    )
    num_years_aus = models.IntegerField(
        label='''Number of years living in Australia (if 
            you have been in Australia less than one year, 
            write zero)''', 
        min=0
    )
    twoB_answer = models.IntegerField(
        label='''If you were to do this experiment again, would 
        you be likely to give different answers in Task 2B (the 
        task where you indicated your willingness to accept the 
        opposing statement for money)?''',
        choices=Constants.likert_different,
        widget=widgets.RadioSelect
    )
    twoB_explain = models.LongStringField(
        label='''Please explain your answer to the previous 
            question.'''
    )
    hypothesis = models.LongStringField(
        label='''What hypothesis do you think the researchers 
            in this experiment are trying to investigate?'''
    )