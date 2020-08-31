from os import environ

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = {
    'real_world_currency_per_point': 0.01,
    'participation_fee': 10,
    'doc': "",
}

SESSION_CONFIGS = [
    {
        'name': 'seg1',
        'display_name': "Segregation",
        'num_demo_participants': 8,  # todo: original = 8?
        'app_sequence': [  # todo: change
            'start',
            'ret',
            'task1',
            'task2',
            'demographic_survey',
            'end',
        ],
        'treatment': 1,
        'ret_time': 90,  # todo: original = 90?
    },
    {
        'name': 'seg2',
        'display_name': "Segregation (NoPun Treatment)",
        'num_demo_participants': 8,
        'app_sequence': [
            'start',
            'ret',
            'task1',
            'task2',
            'demographic_survey',
            'end',
        ],
        'treatment': 2,
        'ret_time': 90,  # todo: original = 90?
    },
    {
        'name': 'ret_test',
        'display_name': "ret",
        'num_demo_participants': 1,
        'app_sequence': [
            'ret',
        ],
        'ret_time': 90,
    },
]

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'AUD'
USE_POINTS = True

ROOMS = []

# AUTH_LEVEL:
# this setting controls which parts of your site are freely accessible,
# and which are password protected:
# - If it's not set (the default), then the whole site is freely accessible.
# - If you are launching a study and want visitors to only be able to
#   play your app if you provided them with a start link, set it to STUDY.
# - If you would like to put your site online in public demo mode where
#   anybody can play a demo version of your game, but not access the rest
#   of the admin interface, set it to DEMO.

# for flexibility, you can set it in the environment variable OTREE_AUTH_LEVEL
AUTH_LEVEL = environ.get('OTREE_AUTH_LEVEL')

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

# don't share this with anybody.
SECRET_KEY = '=6a3l*&&1tc-^r=a8x7_!=ne3-&2s3me1wzf(54@v6d9n5tn3t'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']

REAL_WORLD_CURRENCY_DECIMAL_PLACES = 2
