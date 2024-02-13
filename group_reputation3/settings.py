from os import environ

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = {
    "real_world_currency_per_point": 0.3,
    "participation_fee": 15.00,
    "doc": "",
}

SESSION_CONFIGS = [
    {
        "name": "gr",
        "display_name": "Group Reputation",
        "num_demo_participants": 9,
        "app_sequence": ["start", "task1", "task2", "ds", "end"],
        "rep_condition": True,
        "deterrence": True,
        "online_exp": False,
        "chosen_task": 1,
        # Uncomment this to enable bots to test in browser. NOTE: The
        # variables in .dev.env MUST be set to 0 in order for this to work
        # "use_browser_bots": True,
    },
]

ROOMS = [
    {
        'name':'toby_lab',
        'display_name':"Toby's Lab",
        'participant_label_file':'lab_number.txt',
    },
]


# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = "en"

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = "AUD"
USE_POINTS = True
POINTS_DECIMAL_PLACES = 2

ADMIN_USERNAME = "admin"
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get("OTREE_ADMIN_PASSWORD")

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = "82_*83%e166-+z+f9-ac4of_*(!oj3!*v7-)qot-#0ud8ef)de"

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ["otree"]
