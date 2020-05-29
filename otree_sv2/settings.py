from os import environ

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = {
    'real_world_currency_per_point': 1.00,
    'participation_fee': 15.00,
    'doc': "",
}

SESSION_CONFIGS = [
    {
       'name': 'ul',
       'display_name': "Ultimatum Treatment",
       'num_demo_participants': 2,
       'app_sequence': [
           'welcome',
           't1u',
           't2_parta', 't2_partb',
           't3', 't3u',
           't4',
           'survey',
           'final'
       ],
       # 'use_browser_bots': True # todo: delete
    },
    {
       'name': 'tr',
       'display_name': "Trust Treatment",
       'num_demo_participants': 2,
       'app_sequence': [
           'welcome',
           't1t',
           't2_parta', 't2_partb',
           't3', 't3t',
           't4',
           'survey',
           'final'
       ],
       # 'use_browser_bots': True # todo: delete
    },
    {
       'name': 't1u',
       'display_name': "Task 1 (Ultimatum)",
       'num_demo_participants': 2,
       'app_sequence': [
           't1u',
       ],
    },
    {
       'name': 't1t',
       'display_name': "Task 1 (Trust)",
       'num_demo_participants': 2,
       'app_sequence': [
           't1t',
       ],
    },
    {
       'name': 't2_3u',
       'display_name': "Task 2 + 3 (Ultimatum)",
       'num_demo_participants': 2,
       'app_sequence': [
           't2_parta', 't2_partb',
           't3', 't3u',
       ],
    },
    {
       'name': 't2_3t',
       'display_name': "Task 2 + 3 (Trust)",
       'num_demo_participants': 2,
       'app_sequence': [
           't2_parta', 't2_partb',
           't3', 't3t',
       ],
    },
    {
       'name': 't4',
       'display_name': "Task 4",
       'num_demo_participants': 1,
       'app_sequence': [
           't4',
       ],
    },
    {
       'name': 'survey',
       'display_name': "Survey",
       'num_demo_participants': 1,
       'app_sequence': [
           'survey',
       ],
    },
]


# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True
POINTS_DECIMAL_PLACES = 1

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


# Consider '', None, and '0' to be empty/false
DEBUG = 0   # (environ.get('OTREE_PRODUCTION') in {None, '', '0'})

DEMO_PAGE_INTRO_HTML = """ """

# don't share this with anybody.
SECRET_KEY = 'bh9ik)41%1z$^lmb(txbd!lr6-y@ndtv3c^d*ln_jsrj9!e-$p'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']
