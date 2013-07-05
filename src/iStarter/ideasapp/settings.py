from iStarter.settings import *

CLASSIFICATIONS = ([
                    ('UNCLASSIFIED', 'UNCLASSIFIED'),
                    ('RESTRICTED',   'RESTRICTED'),
                    ('CONFIDENTIAL', 'CONFIDENTIAL'),
                    ('SECRET',       'SECRET'),
                    ('TOP SECRET',   'TOP SECRET'),
                    ])


#Template for model outputs
TEMPLATE_HEADINGS = [{'db':'pk', 'pretty':'ID'}, 
                     {'db':'title', 'pretty':'Idea Title'}, 
                     {'db':'pub_date', 'pretty':'Date Published'},
                     {'db':'description', 'pretty':'Idea Description'},
                     {'db':'likes', 'pretty':'Likes'},
                     {'db':'dislikes', 'pretty':'Disikes'},]


SORT_URL_KEY_NAME = 'sort'
TAG_URL_KEY_NAME = 'tags'

# These are the valid sort fields and their pretty names - typically continuous values
VALID_SORT_FIELDS = {'pub_date'         : 'Published Date',
                     'title'            : 'Title',
                     'num_likes'        : 'Likes',
                     'num_dislikes'     : 'Dislikes'}    

# These are the fields you might want to filter on - typically more discrete values               
VALID_FILTERS =      {'classification' : [i[0] for i in CLASSIFICATIONS]}

# All together now - keeping these separate allows us to check against them in different ways
VALID_FILTER_PARAMS = {SORT_URL_KEY_NAME : VALID_SORT_FIELDS,
                       TAG_URL_KEY_NAME  : None}
VALID_FILTER_PARAMS.update(VALID_FILTERS)