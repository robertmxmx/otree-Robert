from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import random


class AllWait(WaitPage):
    wait_for_all_groups = True


class Instructions(Page):
    pass


class Ranking(Page):
    timeout_seconds = 4*60
    timeout_submission = {k: 0 for k in ['conceal'+str(i) for i in range(1, Constants.s_total+1)]}
    form_model = 'player'
    form_fields = ['conceal'+str(i) for i in range(1, Constants.s_total+1)]

    def vars_for_template(self):
        s_subset = [self.participant.vars['sp_data'].copy()[i] for i in Constants.statement_list]
        random.shuffle(s_subset)

        with open(Constants.list_of_statements_file, 'a') as f:
            f.write("PARTICIPANT_ID: " + str(self.participant.id_in_session) + "\n")
            for statement in s_subset:
                f.write(statement + "\n")
            f.write("\n")

        self.participant.vars['s_revealed'] = s_subset.copy()
        return {
            's_subset': self.participant.vars['s_revealed']
        }

    def error_message(self, values):
        sorted_input = [x for x in values.values() if x is not None]
        if sorted(sorted_input) != [i for i in range(1, len(sorted_input)+1)]:
            return 'invalid input'


class ProcessingPage(WaitPage):

    def after_all_players_arrive(self):
        if self.session.config['treatment'] == 1:
            self.group.set_random_conceal()
            for p in self.group.get_players():
                p.set_revealed()


class ConcealDecision(Page):

    def vars_for_template(self):
        return_dict = {'treatment': self.session.config['treatment']}
        if self.session.config['treatment'] == 1:
            return_dict.update({
                'num_random_conceal': self.group.num_random_conceal,
                'num_to_reveal': Constants.s_total - self.group.num_random_conceal,
                'num_chosen': self.player.num_chosen,
                'num_to_conceal': min(self.player.num_chosen, self.group.num_random_conceal)
            })
        return return_dict


class InformationRevealed(Page):

    def vars_for_template(self):
        partner_statements = self.player.get_others_in_group()[0].participant.vars['s_revealed']
        player_statements = self.participant.vars['s_revealed']
        return {
            'num_partner': len(partner_statements),
            'partner_statements': partner_statements,
            'num_player': len(player_statements),
            'player_statements': player_statements
        }


page_sequence = [
    AllWait,

    Instructions,
    Ranking,
    ProcessingPage,
    ConcealDecision,
    InformationRevealed,
]