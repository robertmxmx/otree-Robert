from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):
    def play_round(self):
        yield (pages.Survey, dict(
            similar1=1, similar2=1, similar3=1, similar4=1, similar5=1,
            similar6=1, similar7=1, similar8=1, similar9=1, similar10=1,
            similar11=1, sex="Male", age=10, area_of_study="Accounting",
            num_exps=2, religion="Hindu", birth_country="Singapore",
            # birth_country_other=None, 
            num_years_aus=2, twoB_answer=5,
            twoB_explain="no", hypothesis="idk"
        ))
