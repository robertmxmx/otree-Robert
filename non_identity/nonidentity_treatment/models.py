from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random, os


author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'nonidentity_treatment'
    players_per_group = None
    num_rounds = 1

    t1_instructions_content = 'nonidentity_treatment/Task1InstructionsContent.html'
    t2a_instructions_content = 'nonidentity_treatment/Task2aInstructionsContent.html'
    t2b_instructions_content = 'nonidentity_treatment/Task2bInstructionsContent.html'
    t2c_instructions_content = 'nonidentity_treatment/Task2cInstructionsContent.html'

    input_ids_file = os.path.abspath('nonidentity_treatment/_input_ids.csv')
    likert_questions_file = '_likert_questions.txt'

    table_style = """
        <style type="text/css">
            table {
                border-collapse: collapse;
                width: 100%;
                table-layout: fixed;
            }
            th {
                border: 1px solid #dddddd;
                background-color: #dddddd;
            }
            td {
                border: 1px solid #dddddd;
            }
        </style>
    """
    t2a_v1_table = table_style + """
        <h5>Version 1</h5>
        <table cellpadding="10">
            <tr>
                <th>You Choose</th>
                <th>You Receive</th>
                <th>Other Participant Receives</th>
            </tr>
            <tr>
                <td>Option 1</td>
                <td>$10</td>
                <td>$10</td>
            </tr>
            <tr>
                <td>Option 2</td>
                <td>$12</td>
                <td>$2</td>
            </tr>
        </table>
    """
    t2a_v2_table = table_style + """
        <h5>Version 2</h5>
        <table cellpadding="10">
            <tr>
                <th>You Choose</th>
                <th>You Receive</th>
                <th>Other Participant Receives</th>
            </tr>
            <tr>
                <td>Option 1</td>
                <td>$10</td>
                <td>$2</td>
            </tr>
            <tr>
                <td>Option 2</td>
                <td>$12</td>
                <td>$10</td>
            </tr>
        </table>
    """
    t2a_table = table_style + """
        <table  cellpadding="8">
            <tr>
                <td style="border: 0px solid black;">
                    """ + t2a_v1_table + """
                </td>
                <td style="border: 0px solid black;">
                    """ + t2a_v2_table + """
                </td>
            </tr>
        </table>
    """

class Subsession(BaseSubsession):
    def creating_session(self):
        #  Read IDs
        with open(Constants.input_ids_file, 'r') as f:
            ids = f.read().splitlines()
        random.shuffle(ids)

        # Allocate IDs, set versions and sub-tasks
        for p in self.get_players():
            p.t1_participantA_id = ids.pop()
            p.t1_participantB_id = ids.pop()
            p.t2_partner_id = ids.pop()
            p.t2a_version = random.randint(1, 2)
            p.t2_chosen_task = random.choice(['a', 'b', 'c'])


class Group(BaseGroup):
    pass


def make_op_field():
    return models.IntegerField(
        choices=[[1, 'Option 1'], [2, 'Option 2']],
        widget=widgets.RadioSelect
    )


class Player(BasePlayer):
    """ Task 1 """
    # Comprehension 1
    t1_c1_1 = models.IntegerField()
    t1_c1_2 = models.IntegerField()
    t1_c1_3 = models.IntegerField()
    t1_c1_wrong = models.IntegerField(initial=0)
    # Comprehension 2
    t1_c2_1 = models.IntegerField()
    t1_c2_2 = models.IntegerField()
    t1_c2_3 = models.IntegerField()
    t1_c2_wrong = models.IntegerField(initial=0)
    # Comprehension 3
    t1_c3 = models.IntegerField(
        choices=[[1, 'Yes'], [2, 'No']],
        widget=widgets.RadioSelect
    )
    t1_c3_wrong = models.IntegerField(initial=0)
    # Main
    t1_option = make_op_field()
    t1_payoff = models.CurrencyField()
    t1_participantA_id = models.StringField()
    t1_participantA_payoff = models.CurrencyField()
    t1_participantB_id = models.StringField()
    t1_participantB_payoff = models.CurrencyField()

    """ Task 2 """
    t2_chosen_task = models.StringField()
    t2_partner_id = models.StringField()

    ''' Task 2a '''
    # Comprehension 1
    t2a_c1 = make_op_field()
    t2a_c1_wrong = models.IntegerField(initial=0)
    # Comprehension 2
    t2a_c2 = models.IntegerField(
        choices=[[1, '$10 for sure'], [2, '$2 for sure'], [3, 'Either $10 or $2, it\'s a matter of chance']],
        widget=widgets.RadioSelect
    )
    t2a_c2_wrong = models.IntegerField(initial=0)
    # Comprehension 3
    t2a_c3 = models.IntegerField(
        choices=[[1, 'Yes'], [2, 'No']],
        widget=widgets.RadioSelect
    )
    t2a_c3_wrong = models.IntegerField(initial=0)
    # Main
    t2a_version = models.IntegerField()
    t2a_option = models.IntegerField(
        choices=[[1, 'Option 1'], [2, 'Option 2'], [3, 'Reveal']],
        widget=widgets.RadioSelect
    )
    t2a_revealed_option = make_op_field()
    t2a_payoff = models.CurrencyField()
    t2a_partner_payoff = models.CurrencyField()

    ''' Task 2b '''
    # Comprehension 1
    t2b_c1_1 = models.IntegerField()
    t2b_c1_2 = models.IntegerField()
    t2b_c1_wrong = models.IntegerField(initial=0)
    # Comprehension 2
    t2b_c2_1 = models.IntegerField()
    t2b_c2_2 = models.IntegerField()
    t2b_c2_wrong = models.IntegerField(initial=0)
    # Main
    t2b_option = make_op_field()
    t2b_payoff = models.CurrencyField()
    t2b_partner_payoff = models.CurrencyField()

    ''' Task 2c '''
    # Comprehension 1
    t2c_c1_1 = models.IntegerField()
    t2c_c1_2 = models.IntegerField()
    t2c_c1_wrong = models.IntegerField(initial=0)
    # Comprehension 2
    t2c_c2_1 = models.IntegerField()
    t2c_c2_2 = models.IntegerField()
    t2c_c2_wrong = models.IntegerField(initial=0)
    # Main
    t2c_option = make_op_field()
    t2c_payoff = models.CurrencyField()
    t2c_partner_payoff = models.CurrencyField()

    @staticmethod
    def set_op_payoff(t1, version, option):
        invalid_option = ValueError("Option is not 1 or 2")
        if t1:
            if option == 1:
                return c(10), c(10), c(0)
            elif option == 2:
                return c(12), c(0), c(2)
            else:
                raise invalid_option
        else:
            if version == 1:
                if option == 1:
                    return c(10), c(10)
                elif option == 2:
                    return c(12), c(2)
                else:
                    raise invalid_option
            elif version == 2:
                if option == 1:
                    return c(10), c(2)
                elif option == 2:
                    return c(12), c(10)
                else:
                    raise invalid_option
            else:
                raise ValueError("Version is not 1 or 2")

    def set_payoff(self):
        self.participant.vars['t1_payoff'] = self.t1_payoff

        if self.t1_participantA_payoff != c(0):
            self.participant.vars['t1_payed_partner'] = 'A'
        elif self.t1_participantB_payoff != c(0):
            self.participant.vars['t1_payed_partner'] = 'B'
        else:
            raise ValueError('A participant was not given $0')

        if self.t2_chosen_task == 'a':
            self.participant.vars['t2_payoff'] = self.t2a_payoff
            self.participant.vars['t2_chosen_task_option'] = self.t2a_option
        elif self.t2_chosen_task == 'b':
            self.participant.vars['t2_payoff'] = self.t2b_payoff
            self.participant.vars['t2_chosen_task_option'] = self.t2b_option
        elif self.t2_chosen_task == 'c':
            self.participant.vars['t2_payoff'] = self.t2c_payoff
            self.participant.vars['t2_chosen_task_option'] = self.t2c_option
        else:
            raise ValueError('Invalid Task 2 sub-task chosen')

        self.participant.vars['t2_chosen_task'] = self.t2_chosen_task
        self.payoff = self.participant.vars['t1_payoff'] + self.participant.vars['t2_payoff']
