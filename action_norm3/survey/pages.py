from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import random


class Main(Page):
    form_model = 'player'
    form_fields = ['sex', 'age', 'area_of_study', 'area_of_study_other', 'num_exps', 'religion',
                   'religion_other', 'birth_country', 'birth_country_other', 'num_years_aus']

    def error_message(self, values):

        # when a player chose the 'Other' option in a question, but did not write in the other field for that question
        other_blank = (values['area_of_study'] == "Other" and values['area_of_study_other'] is None) or \
                      (values['religion'] == "Other" and values['religion_other'] is None) or \
                      (values['birth_country'] == "Other" and values['birth_country_other'] is None)

        if other_blank:
            return "You chose 'Other' as an answer, but failed to write in the other field for that question"

    def before_next_page(self):
        # clears the other fields if user did not choose 'Other'
        if self.player.area_of_study != "Other":
            self.player.area_of_study_other = None
        if self.player.religion != "Other":
            self.player.religion_other = None
        if self.player.birth_country != "Other":
            self.player.birth_country_other = None


class Main2(Page):
    form_model = 'player'

    def get_form_fields(self):
        apps_list = self.session.config['app_sequence'].copy()
        if 'oneRtwoG' in apps_list and 'twoRoneG' in apps_list:
            return ['q1', 'q2', 'q3', 'q4']
        else:
            return ['q1', 'q2']

    def vars_for_template(self):
        apps_list = self.session.config['app_sequence'].copy()
        if 'oneRtwoG' in apps_list and 'twoRoneG' in apps_list:
            oneRtwoG_num = apps_list.index('oneRtwoG')
            twoRoneG_num = apps_list.index('twoRoneG')
            return {'task2': ("2R1G" if oneRtwoG_num < twoRoneG_num else "1R2G")}
        else:
            return {'task2': None}


class Main3(Page):
    form_model = 'player'

    def get_form_fields(self):
        apps_list = self.session.config['app_sequence'].copy()
        fields = ['survey_cause_explain']

        if 'twoRoneG' in apps_list:
            fields += ['survey_cause_red1', 'survey_cause_green1']
        if 'oneRtwoG' in apps_list:
            fields += ['survey_cause_red2', 'survey_cause_green2']
        if 'twoRtwoG' in apps_list:
            fields += ['survey_cause_red3', 'survey_cause_green3']

        return fields

    def vars_for_template(self):
        apps_list = self.session.config['app_sequence'].copy()
        questions = []

        if 'twoRoneG' in apps_list:         # if 2r1g was played, add the questions regarding it
            questions.append(Constants.name_in_url + '/2R1GQuestion.html')
        if 'oneRtwoG' in apps_list:         # same for 1r2g
            questions.append(Constants.name_in_url + '/1R2GQuestion.html')
        if 'twoRtwoG' in apps_list:         # same for 2r2g
            questions.append(Constants.name_in_url + '/2R2GQuestion.html')

        random.shuffle(questions)           # shuffle the sets of questions
        return {'questions': questions}


page_sequence = [
    Main,
    Main2,
    Main3
]
