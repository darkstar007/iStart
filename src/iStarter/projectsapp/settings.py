from iStarter.settings import *

CLASSIFICATIONS = ([
                    ('UNCLASSIFIED', 'UNCLASSIFIED'),
                    ('RESTRICTED',   'RESTRICTED'),
                    ('CONFIDENTIAL', 'CONFIDENTIAL'),
                    ('SECRET',       'SECRET'),
                    ('TOP SECRET',   'TOP SECRET'),
                    ])

# Can modify this to change the range of options available for the project rating levels (importance, resource, effort)
# Start of range is hard coded at 1 in forms.py
PROJECT_RATING_LEVELS = 6 