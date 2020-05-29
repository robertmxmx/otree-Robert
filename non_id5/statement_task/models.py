from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


class Constants(BaseConstants):
    name_in_url = 'statement_task'
    players_per_group = None
    num_rounds = 1

    neutral_statements = [
        'This laboratory has been operating for over twenty years',
        'This research project is funded by the ARC',
        'The lead researcher of this project obtained his PhD in the USA',
        '''Today’s experiment was intended to study the psychological basis of behaviour that is relevant 
            to environmental conservation policy'''
    ]
    test_statements = [
        'The recipients in task one will be paid in the way described in the instructions'
    ]


class Subsession(BaseSubsession):

    def creating_session(self):
        for p in self.get_players():
            # Subjects with odd group id numbers are shown neutral statements. Subjects with even group id
            # numbers are shown neutral statements + test statement
            p.statement_group = 1 if p.participant.id_in_session % 2 == 1 else 2


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    statement_group = models.IntegerField()
    num_agree = models.IntegerField()
