from os import environ

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']
#EXTENSION_APPS = ['otree_tools']
mturk_hit_settings = {
    'keywords': ['bonus', 'study'],
    'title': 'Title for your experiment',
    'description': 'Description for your experiment',
    'frame_height': 500,
    'preview_template': 'global/MTurkPreview.html',
    'minutes_allotted_per_assignment': 60,
    'expiration_hours': 7 * 24,  # 7 days
    # 'grant_qualification_id': 'YOUR_QUALIFICATION_ID_HERE',# to prevent retakes
    'qualification_requirements': []
}
SESSION_CONFIG_DEFAULTS = {
    'real_world_currency_per_point': 1.00,
    'participation_fee': 2.00,
    'doc': "",
    'mturk_hit_settings': mturk_hit_settings,
}

AWS_ACCESS_KEY_ID = environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = environ.get('AWS_SECRET_ACCESS_KEY')

SESSION_CONFIGS = [
    {
        'name': 'auditquessurv',
        'display_name': "Audit Survey Demo",
        'num_demo_participants': 1,
        'app_sequence': ['auditsurvey']
    },
    {
        'name': 'test_instrument',
        'display_name': "Give it a WHIRL!!",
        'num_demo_participants': 1,
        'app_sequence': ['test_instrument', ],
        # fixed: FX, skewed: SK, symmetric: SM
        'treatment': 'FX',
    },
    {
        'name': 'full_experiment',
        'display_name': "Full Simulation - DRAFT",
        'num_demo_participants': 1,
        'app_sequence': ['modquiz', 'test_instrument', 'auditsurvey'],
        # fixed: FX, skewed: SK, symmetric: SM
        'treatment': 'FX',
    },
    {'name': 'modquiz',
     'display_name': "Charity Earnings Task",
     'num_demo_participants': 1,
     'app_sequence': ['modquiz'],
     },
    {'name': 'entire_exp',
     'display_name': "Charity Math Task",
     'num_demo_participants': 3,
     'app_sequence': ['mathquiz'],
     'treatment': 'DG',
     },
    {'name': 'mathquiz',
     'display_name': "Decoding Task Only",
     'num_demo_participants': 3,
     'app_sequence': ['mathquiz'],
     'treatment': 'DG',
     },
]

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = False

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
DEBUG = (environ.get('OTREE_PRODUCTION') in {None, '', '0'})

DEMO_PAGE_INTRO_HTML = """ """

# don't share this with anybody.
SECRET_KEY = 'foijz^)$ba=$*5uyed+y35cm%yags#u91)*$%&!!e5*1r_^3ha'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree',
                #  'otree_tools'
                  ]
