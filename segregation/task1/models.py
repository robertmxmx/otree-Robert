from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random


class Constants(BaseConstants):
    name_in_url = 'task1'
    players_per_group = 8
    num_rounds = 15  # todo: original = 15

    starting_periods = 3  # todo: original = 3
    starting_points = 600
    red_pts_each_period = 50
    blue_pts_each_period = 150
    max_deduction_pts = 10
    deduction_multiplier = 3


class Subsession(BaseSubsession):

    def creating_session(self):
        if self.round_number == 1:
            for p in self.get_players():
                p.participant.payoff = c(Constants.starting_points)


class Group(BaseGroup):
    num_red = models.IntegerField(initial=0)
    num_blue = models.IntegerField(initial=0)

    # get town and color from previous round
    def get_town_color(self):
        for p in self.get_players():
            if 'town' not in p.participant.vars and 'color' not in p.participant.vars:  # if ret is not run
                if p.id_in_group <= len(self.get_players()) / 2:
                    color = 'red'
                else:
                    color = 'blue'

                p.participant.vars['town'] = color
                p.participant.vars['color'] = color
                p.town = color
                p.color = color
            else:
                p.town = p.participant.vars['town']
                p.color = p.participant.vars['color']

    # set new town of each participant and count number of players in each town
    def set_town_after_move(self):
        for p in self.get_players():
            if p.chose_to_switch:
                p.town = ('blue' if p.town == 'red' else 'red')

            if p.town == 'red':
                self.num_red += 1
            elif p.town == 'blue':
                self.num_blue += 1
            else:
                print("error: invalid town")

    # determines whether in round that player can choose to move or not
    def at_starting_periods(self):
        return self.round_number <= Constants.starting_periods

    # determines whether in round that player can choose to deduct or not
    def at_deduction_round(self):
        return self.session.config['treatment'] == 1 and not self.at_starting_periods()

    # get the town history from previous rounds in game
    def get_town_history(self):
        start_round = 1
        end_round = self.round_number - 1
        town_history = []

        for s in self.in_rounds(start_round, end_round):
            town_history.append(s.get_current_allocation())

        return town_history

    # get current allocation of town
    def get_current_allocation(self):
        red_town = []
        blue_town = []

        for p in self.get_players():
            p_data = {
                'id': p.get_id(),
                'color': p.color,
            }

            if p.pts_from_moving is not None:
                p_data['moving_pts'] = round(p.pts_from_moving)

            if p.pts_deducted is not None:
                p_data['deduction_pts'] = round(p.pts_deducted)

            if p.town == 'red':
                red_town.append(p_data)
            elif p.town == 'blue':
                blue_town.append(p_data)
            else:
                print("error: invalid town")

        return {'red_town': red_town, 'blue_town': blue_town}

    # this is data that is used by a few pages
    def get_common_data(self):
        return {
            'town_history': self.get_town_history(),
            'current_period': self.get_current_allocation(),
        }

    # set the payoff to inhabitants after moving is complete
    def set_payoff_after_move(self):
        red_town_total = 0
        blue_town_total = 0

        for p in self.get_players():
            if p.town == 'red':
                if p.color == 'red':
                    red_town_total += Constants.red_pts_each_period
                elif p.color == 'blue':
                    red_town_total += Constants.blue_pts_each_period
            elif p.town == 'blue':
                if p.color == 'red':
                    blue_town_total += Constants.red_pts_each_period
                elif p.color == 'blue':
                    blue_town_total += Constants.blue_pts_each_period
            else:
                print("error: invalid town")

        red_town_payoff = c((red_town_total / self.num_red) if self.num_red != 0 else 0)
        blue_town_payoff = c((blue_town_total / self.num_blue) if self.num_blue != 0 else 0)

        for p in self.get_players():
            if p.town == 'red':
                p.pts_from_moving = red_town_payoff
            elif p.town == 'blue':
                p.pts_from_moving = blue_town_payoff
            else:
                print("error: invalid color")
            p.payoff += p.pts_from_moving

    # distribute deduction points
    def set_payoff_after_deduct(self):
        for p in self.get_players():
            pts_p_received = 0
            pts_p_assigned = 0

            for g in self.get_players():
                g_assigned = [
                    g.deduct1, g.deduct2, g.deduct3, g.deduct4, g.deduct5, g.deduct6, g.deduct7, g.deduct8
                ]
                pts_p_received += g_assigned[p.id_in_group - 1] if g_assigned[p.id_in_group - 1] else 0

                if g == p:
                    pts_p_assigned = sum([x for x in g_assigned if x])

            p.pts_deducted = c(Constants.deduction_multiplier * pts_p_received)
            p.pts_assigned = c(pts_p_assigned)

            p.payoff -= p.pts_deducted + p.pts_assigned


class Player(BasePlayer):
    color = models.StringField()  # the color that a player will be displayed as
    town = models.StringField()  # the town that the player will reside in
    chose_to_switch = models.BooleanField(
        label='Which town do you wish to move to?',
        widget=widgets.RadioSelect,
    )
    pts_from_moving = models.CurrencyField()
    move_timed_out = models.BooleanField()
    pts_deducted = models.CurrencyField()
    pts_assigned = models.CurrencyField()
    deduct1 = models.CurrencyField(min=0, max=Constants.max_deduction_pts)
    deduct2 = models.CurrencyField(min=0, max=Constants.max_deduction_pts)
    deduct3 = models.CurrencyField(min=0, max=Constants.max_deduction_pts)
    deduct4 = models.CurrencyField(min=0, max=Constants.max_deduction_pts)
    deduct5 = models.CurrencyField(min=0, max=Constants.max_deduction_pts)
    deduct6 = models.CurrencyField(min=0, max=Constants.max_deduction_pts)
    deduct7 = models.CurrencyField(min=0, max=Constants.max_deduction_pts)
    deduct8 = models.CurrencyField(min=0, max=Constants.max_deduction_pts)
    deduction_timed_out = models.BooleanField()

    def deducted_pts_before_multiply(self):
        return int(self.pts_deducted / Constants.deduction_multiplier)

    def get_id(self):
        if self.color == 'red':
            return 'R' + str(self.id_in_group)
        else:
            return 'B' + str(self.id_in_group)

    # find others in same town
    def create_town_pop_deduction_fields(self):
        town_pop = []
        deduction_fields = []

        for p in self.group.get_players():
            if p.town == self.town and p != self:
                deduction_fields.append('deduct' + str(p.id_in_group))
                town_pop.append({
                    'color': p.color,
                    'id': p.get_id(),
                    'raw_id': p.id_in_group,
                })

        self.participant.vars['town_pop'] = town_pop.copy()
        self.participant.vars['deduction_fields'] = deduction_fields.copy()

    # randomly decide whether a player switched towns if they time out on the move decision page
    def move_timeout_action(self):
        self.move_timed_out = True
        self.chose_to_switch = random.choice([True, False])

    # set all deduction fields to 0 if player timed out
    def deduct_timeout_action(self):
        self.deduction_timed_out = True

        self.deduct1 = self.deduct2 = self.deduct3 = self.deduct4 = self.deduct5 = self.deduct6 = self.deduct7 = \
            self.deduct8 = c(0)

    # sets payoff for end of task
    def finalize(self):
        self.participant.vars['town'] = self.town

        if self.participant.payoff < c(0):
            self.participant.payoff = c(0)

        self.participant.vars["task1_payoff"] = self.participant.payoff
