from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class PartAInstructions(Page):
    pass


class PartA(Page):
    form_model = 'player'

    def get_form_fields(self):
        return [ self.player.get_current_statement() ]

    def error_message(self, values):
        # this is a hack to dynamically get and store the statement chosen data.
        # it is done inside error_message as this method provides 'values',
        # a dictionary that I can get the data I need using strings (statement)
        statement = self.player.get_current_statement()
        self.participant.vars['statements'][statement] = values[statement]

    def before_next_page(self):
        self.participant.vars['current_statement'] += 1


class PartBInstructions(Page):
    def before_next_page(self):
        self.participant.vars['current_statement'] = 0


class PartB(Page):
    form_model = 'player'

    def get_form_fields(self):
        return [ self.player.get_current_statement() + "_bid" ]

    def vars_for_template(self):
        statement = self.player.get_current_statement()

        accepted_statement_index = self.participant.vars['statements'][statement]
        statement_info = Constants.statements[statement]

        accepted_statement = statement_info[accepted_statement_index-1][1]
        opposite_statement = statement_info[accepted_statement_index-2][1]

        return dict(
            accepted_statement=accepted_statement,
            opposite_statement=opposite_statement
        )

    def error_message(self, values):
        statement = self.player.get_current_statement()
        bid = values[ statement + "_bid" ]

        valid_range = [ str(_) for _ in range(Constants.min_bid, Constants.max_bid + 1) ]
        
        if bid not in valid_range and bid != Constants.opt_out_text:
            return '''Amount must be a number from %s to %s or "%s"
                ''' % (Constants.min_bid, Constants.max_bid, Constants.opt_out_text)
        
        self.participant.vars['statements_bid'][statement] = bid


    def before_next_page(self):
        self.participant.vars['current_statement'] += 1


class PartBOutcome(Page):
    pass

page_sequence = [
    PartAInstructions,
] + [ PartA for _ in range(len(Constants.statements))] + [
    PartBInstructions
] + [ PartB for _ in range(len(Constants.statements))] + [
    PartBOutcome
]
