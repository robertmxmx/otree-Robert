from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Survey(Page):
    form_model = 'player'
    form_fields = [ 
        'similar1', 'similar2', 'similar3', 'similar4', 'similar5', 
        'similar6', 'similar7', 'similar8', 'similar9', 'similar10', 
        'similar11', 'sex', 'age', 'area_of_study', 'num_exps', 
        'religion', 'birth_country', 'birth_country_other', 
        'num_years_aus', 'twoB_answer', 'twoB_explain', 'hypothesis'
    ]

    def error_message(self, values):

        if values['birth_country'] == "Other:" and values['birth_country_other'] is None:
            return '''You chose 'Other' as an answer, but failed to fill in
                the other field for that question'''


page_sequence = [
    Survey
]
