from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants

class Consent(Page):
    form_model = 'player'
    form_fields = ['name','accept']

page_sequence = [
    Consent,
    ]
    