from os import environ

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = {
    'real_world_currency_per_point': 1.00,
    'participation_fee': 0.00,
    'doc': "",
}

SESSION_CONFIGS = [
    {
       'name': 'ni',
       'display_name': "Non-Identity",
       'num_demo_participants': 2,
       'app_sequence': [
           'start',
           'main_task',
           'statement_task',
           'morals_task',
           'demographic_survey',
           'end'
       ],
       'use_browser_bots': False,   # todo: change to false
    },
]


# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'AUD'
REAL_WORLD_CURRENCY_DECIMAL_PLACES = 0
USE_POINTS = False

ROOMS = []

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEBUG = 0

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = 'snw8xs8t2mvs&id4lf-rxt+=1dx!a#m1=17y&vw6z=2h*z%j@9'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']
