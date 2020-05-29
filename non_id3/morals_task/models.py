from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


class Constants(BaseConstants):
    name_in_url = 'morals_task'
    players_per_group = None
    num_rounds = 1

    question_labels = [
        '''
            If the only way to save another person’s life during an emergency is to sacrifice one’s own leg, then one 
            is morally required to make this sacrifice
        ''',
        '''
            From a moral point of view, we should feel obliged to give one of our kidneys to a person with kidney 
            failure since we don’t need two kidneys to survive, but really only one to be healthy
        ''',
        '''
            From a moral perspective, people should care about the well-being of all human beings on the planet 
            equally; they should not favour the well-being of people who are especially close to them either 
            physically or emotionally
        ''',
        '''
            It is just as wrong to fail to help someone as it is to actively harm them yourself
        ''',
        '''
            It is morally wrong to keep money that one doesn't really need if one can donate it to causes that provide 
            effective help to those who will benefit a great deal
        ''',
        '''
            It is morally right to harm an innocent person if harming them is a necessary means to helping several 
            other innocent people
        ''',
        '''
            If the only way to ensure the overall well-being and happiness of the people is through the use of political 
            oppression for a short, limited period, then political oppression should be used
        ''',
        '''
            It is permissible to torture an innocent person if this would be necessary to provide information to prevent 
            a bomb going off that would kill hundreds of people
        ''',
        '''
            Sometimes it is morally necessary for innocent people to die as collateral damage—if more people are 
            saved overall
        '''
    ]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


def create_field():
    for q_label in Constants.question_labels:
        yield models.StringField(
            label=q_label,
            choices=[
                'Strongly Disagree', 'Disagree', 'Somewhat Disagree', 'Neither Agree Nor Disagree',
                'Somewhat Agree', 'Agree', 'Strongly Agree'
            ],
            widget=widgets.RadioSelect
        )


next_q = create_field()


class Player(BasePlayer):
    q1 = next(next_q)
    q2 = next(next_q)
    q3 = next(next_q)
    q4 = next(next_q)
    q5 = next(next_q)
    q6 = next(next_q)
    q7 = next(next_q)
    q8 = next(next_q)
    q9 = next(next_q)
