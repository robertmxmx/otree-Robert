from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
from otree.api import Submission


class PlayerBot(Bot):

    def play_round(self):
        print("In each of your responses, we would like you to answer as truthfully as possible, <b>based on your" in self.html)
        yield (pages.Instructions)

        yield (pages.Comprehension, {
            'comp1': "$0" if self.subsession.this_task1 else "$10",
            'comp2': "$10"
        })

        if self.round_number == 1:
            yield Submission(pages.Scenario, check_html=False)

            if self.session.config['treatment'] == 1:
                yield (pages.ScenarioComprehension, {
                    't_comp1a': 12, 't_comp1b': 0, 't_comp1c': 2,
                    't_comp2a': 10, 't_comp2b': 10, 't_comp2c': 0,
                    't_comp3': "No"
                })
            else:
                yield (pages.ScenarioComprehension, {
                    'c_comp1a': 10, 'c_comp1b': 10,
                    'c_comp2a': 12, 'c_comp2b': 2
                })

        if self.participant.id_in_session <= 2:
            yield (pages.Choice, {
                'option1': "Very socially appropriate",
                'option2': "Very socially inappropriate"
            })
        elif self.participant.id_in_session <= 4:
            yield (pages.Choice, {
                'option1': "Somewhat appropriate",
                'option2': "Somewhat inappropriate"
            })
        elif self.participant.id_in_session == 5:
            yield (pages.Choice, {
                'option1': "Somewhat inappropriate",
                'option2': "Somewhat appropriate"
            })
        else:
            yield (pages.Choice, {
                'option1': "Very socially inappropriate",
                'option2': "Very socially appropriate"
            })
