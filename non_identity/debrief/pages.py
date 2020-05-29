from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import csv


class Main(Page):

    def vars_for_template(self):
        return_dict = {
            'total_payoff': self.player.to_c(self.participant.payoff_plus_participation_fee()),
            'treatment': self.session.config['treatment']
        }

        with open(Constants.venue_info_file, 'r') as f:
            csv_f = list(csv.reader(f))

        if self.session.config['treatment'] == 1:
            t1_payoff = self.participant.payoff

            venue_location = csv_f[0][0]
            venue_date = csv_f[0][1]
            venue_time = csv_f[0][2]

            return_dict.update({
                't1_payoff': self.player.to_c(t1_payoff),
                'venue_location': venue_location,
                'venue_date': venue_date,
                'venue_time': venue_time,
            })
        elif self.session.config['treatment'] == 2:
            t1_payoff = self.participant.vars['t1_payoff']
            t2_payoff = self.participant.vars['t2_payoff']

            venue_location1, venue_date1, venue_time1 = csv_f[1][0], csv_f[1][1], csv_f[1][2]
            if self.participant.vars['t2_chosen_task'] == 'a':
                venue_location2, venue_date2, venue_time2 = csv_f[2][0], csv_f[2][1], csv_f[2][2]
            elif self.participant.vars['t2_chosen_task'] == 'b':
                venue_location2, venue_date2, venue_time2 = csv_f[3][0], csv_f[3][1], csv_f[3][2]
            elif self.participant.vars['t2_chosen_task'] == 'c':
                venue_location2, venue_date2, venue_time2 = csv_f[4][0], csv_f[4][1], csv_f[4][2]
            else:
                raise ValueError("Incorrect value for t2_chosen_task")

            return_dict.update({
                't2_chosen_task': self.participant.vars['t2_chosen_task'].upper(),
                't2_chosen_task_option': self.participant.vars['t2_chosen_task_option'],
                't1_payoff': self.player.to_c(t1_payoff),
                't2_payoff': self.player.to_c(t2_payoff),
                't1_payed_partner': self.participant.vars['t1_payed_partner'],
                'venue_location1': venue_location1,
                'venue_date1': venue_date1,
                'venue_time1': venue_time1,
                'venue_location2': venue_location2,
                'venue_date2': venue_date2,
                'venue_time2': venue_time2
            })
        else:
            raise ValueError("Incorrect value for treatment")

        return return_dict


page_sequence = [Main]
