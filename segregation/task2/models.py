from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random


class Constants(BaseConstants):
    name_in_url = 'task2'
    players_per_group = 8
    num_rounds = 15  # todo: original = 15

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


class Player(BasePlayer):
    color = models.StringField()  # the color that a player will be displayed as
    town = models.StringField()  # the town that the player will reside in
    chose_to_switch = models.BooleanField(
        label='Which town do you wish to move to?',
        widget=widgets.RadioSelect,
    )
    pts_from_moving = models.CurrencyField()
    move_timed_out = models.BooleanField()

    def get_id(self):
        if self.color == 'red':
            return 'R' + str(self.id_in_group)
        else:
            return 'B' + str(self.id_in_group)

    # randomly decide whether a player switched towns if they time out on the move decision page
    def move_timeout_action(self):
        self.move_timed_out = True
        self.chose_to_switch = random.choice([True, False])

    # sets payoff for end of task
    def finalize(self):
        self.participant.vars['town'] = self.town

        if self.participant.payoff < c(0):
            self.participant.payoff = c(0)

        self.participant.vars["task2_payoff"] = self.participant.payoff
