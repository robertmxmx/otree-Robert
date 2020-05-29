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
       'name': 'non_id',
       'display_name': "Non-Identity",
       'num_demo_participants': 2,
       'app_sequence': [
           'start',
           'task1_2',
           'statement_task',        # task 3
           'morals_task',           # task 4
           'values_task',           # task 5
           'demographic_survey',    # task 6
           'end'
       ],
       # 'use_browser_bots': True,      # todo: change
       'treatment': 1,
       'order': 1
    },
]


# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'AUD'
USE_POINTS = False

ROOMS = []

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEBUG = 0

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = 'j@tldr$cn$7b97qij2+cspol%5qa(h=7x_29u&oylm^030sg$z'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']