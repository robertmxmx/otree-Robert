from os import environ

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, 
    participation_fee=10, 
    doc=""
)

SESSION_CONFIGS = [
    dict(
       name='sv',
       display_name="Sacred Values",
       num_demo_participants=2,
       app_sequence=[
           'start',
           'task1',
           'task2',
           'task3',
           'survey',
           'end'
       ],
       treatment='hawkdove'         # possible values: hawkdove,
    ),
]


# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'AUD'
USE_POINTS = True
POINTS_DECIMAL_PLACES = 0

ROOMS = []

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = 'faf!ta034oh+=+9n#x)hz)=@+a5hgtamhrv(%czzurygpsq_&8'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']

# disable debug mode
DEBUG = 0
