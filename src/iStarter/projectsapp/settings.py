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

EFFORT_FIELD = 'effort'
IMPORTANCE_FIELD = 'importance'
RESOURCE_FIELD = 'resource'
NUM_BACKERS = 'num_backers'

#RB: No longer being used by custom retrieval code
VALUES_FIELD = ['title','pub_date','description', 'num_backers', 'pk', 'classification']

#Template for model outputs
TEMPLATE_HEADINGS = [{'db':'pk', 'pretty':'ID'}, 
                     {'db':'title', 'pretty':'Idea Title'}, 
                     {'db':'pub_date', 'pretty':'Date Published'},
                     {'db':'description', 'pretty':'Idea Description'},
                     {'db':'num_backers', 'pretty':'Number of Backers'},
                     {'db':'pk','pretty':'Project Id'},
                     {'db':'importance','pretty':'Importance of task'},
                     {'db':'effort','pretty':'Level of Effort required'},
                     {'db':'resource','pretty':'Resources required'},
                     {'db':'active','pretty':'Project is Active'},
                     {'db':'num_likes','pretty':'Number of Likes'},
                     {'db':'num_dislikes','pretty':'Number of Dislikes'}]


SORT_URL_KEY_NAME = 'sort'
TAG_URL_KEY_NAME = 'tags'

# These are the valid sort fields and their pretty names - typically continuous values
VALID_SORT_FIELDS = {'pub_date'         : 'Published Date',
                     'title'            : 'Title',
                     #'classification'   : 'Classification', -- This removed for the time being as we're storing it as a string and not a sortable field.
                     'num_likes'        : 'Likes',
                     'num_dislikes'     : 'Dislikes',
                     #'mean_likes'       : 'Average Like/Dislike',
                     'num_backers'      : 'Backers',
                     'importance'       : 'Importance', 
                     'effort'           : 'Effort',
                     'resource'         : 'Resource'}
                     #'active'           : 'Active or Inactive'}
    

# These are the fields you might want to filter on - typically more discrete values               
VALID_FILTERS =      {'classification' : [i[0] for i in CLASSIFICATIONS],
                      'importance'     : [str(r) for r in range(1, PROJECT_RATING_LEVELS)],  # Keeps it inline with our rating scale
                      'resource'       : [str(r) for r in range(1, PROJECT_RATING_LEVELS)],  # Keeps it inline with our rating scale
                      'effort'         : [str(r) for r in range(1, PROJECT_RATING_LEVELS)],  # Keeps it inline with our rating scale
                      'active'         : ['1', '0'],
                      'verified'       : ['1', '0']}

# All together now - keeping these separate allows us to check against them in different ways
VALID_FILTER_PARAMS = {SORT_URL_KEY_NAME : VALID_SORT_FIELDS,
                       TAG_URL_KEY_NAME  : None}
VALID_FILTER_PARAMS.update(VALID_FILTERS)