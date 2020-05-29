from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
from otree.api import Submission
import random


class PlayerBot(Bot):

    def play_round(self):
        apps_list = self.session.config['app_sequence'].copy()

        yield (pages.Main, {
            'sex': "Male",
            'age': 10,
            'area_of_study': "Accounting",
            'num_exps': "0",
            'religion': "Hindu",
            'birth_country': "China",
            'num_years_aus': random.choice(list(range(1, 10 + 1)))
        })

        if 'oneRtwoG' in apps_list and 'twoRoneG' in apps_list:
            yield (pages.Main2, {
                'q1': random.choice(list(range(1, 7 + 1))),
                'q2': random.choice(list(range(1, 7 + 1))),
                'q3': random.choice(list(range(1, 7 + 1))),
                'q4': random.choice(list(range(1, 7 + 1)))
            })
        else:
            yield (pages.Main2, {
                'q1': random.choice(list(range(1, 7 + 1))),
                'q2': random.choice(list(range(1, 7 + 1)))
            })

        ans = {'survey_cause_explain': 'blah'}
        if 'oneRtwoG' in apps_list:
            ans.update({
                'survey_cause_red1': random.choice(list(range(1, 7 + 1))),
                'survey_cause_green1': random.choice(list(range(1, 7 + 1)))
            })
        if 'twoRoneG' in apps_list:
            ans.update({
                'survey_cause_red2': random.choice(list(range(1, 7 + 1))),
                'survey_cause_green2': random.choice(list(range(1, 7 + 1)))
            })
        if 'twoRtwoG' in apps_list:
            ans.update({
                'survey_cause_red3': random.choice(list(range(1, 7 + 1))),
                'survey_cause_green3': random.choice(list(range(1, 7 + 1)))
            })
        yield Submission(pages.Main3, ans, check_html=False)
