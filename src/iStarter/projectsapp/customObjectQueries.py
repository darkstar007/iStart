import logging

import projectsapp.settings as settings
from projectsapp.models import project as projectModel

logging.getLogger(__name__)

#------------------------------------------------------------------------

def validateQueryParams(params):
    ''' Checks the query parameters against a known list in app-level settings.py '''
    
    safeParams = {}
    # Loop through our url parameters
    for key, val in params.items():
        
        # Check each of the param keys
        if key not in settings.VALID_FILTER_PARAMS.keys():
            logging.warning('Project Gallery Filter: This URL KEY failed-- %s:%s' %(key, val))
        else:
            # Ignore None values - they're saved for long lists as a string
            if val:
                # Now param check that the value is acceptable 
                if settings.VALID_FILTER_PARAMS[key] and val not in settings.VALID_FILTER_PARAMS[key]:
                    logging.warning('Project Gallery Filter: This URL VALUE failed-- %s:%s' %(key, val))
                else:
                    safeParams[key] = val
            else:
                safeParams[key] = val
    
    return safeParams

#------------------------------------------------------------------------

def tagBasedFilter(resultSet, params):
    ''' Returns results based on the tags provided in URL parameters'''
    
    # Get tag parameter string into a variable
    tagString = params[settings.TAG_URL_KEY_NAME]
    
    # Get tags from string to list
    #TODO: See about an exclude filter for taggit
    queryTags = [t for t in tagString.split(',')]
                
    try:
        # Calls a distinct to ensure we don't get duplicate projects (ie projects that have the same tag)
        resultSet = resultSet.filter(tags__name__in=queryTags).distinct()
    except:
        logging.error('Failed to query on tags: %s'%(', '.join(queryTags)))
        resultSet = None
        
    return resultSet
    
#------------------------------------------------------------------------

def exactMatchFilter(resultSet, params):
    ''' Returns results based on an exact field match.
        This does filter by multiple values.
    '''

    # Build a dictionary to pass into the filter using kwargs
    # http://yuji.wordpress.com/2009/09/12/django-python-dynamically-create-queries-from-a-string-and-the-or-operator/
    for key in params.keys():
        fieldVals = {}
        if key in settings.VALID_FILTERS:
            fieldVals[key] = params[key]
            try:
                resultSet = resultSet.filter(**fieldVals)    
            except:
                logging.error('Failed on field-based filtering. Fields/Values-- %s'%(', '.join(fieldVals.items())))
                resultSet = None
                
    return resultSet

#------------------------------------------------------------------------

def sortedResults(resultSet, params):
    ''' Returns results sorted by a URL parameter.
        This does accept multiple fields to do its sorting by.
    '''
    
    # Get the field user has requested to sort on
    sortValue = params[settings.SORT_URL_KEY_NAME]
    
    # sortValue should look like this: "<fieldName1>;<direction>,<fieldName2>;<direction>"
    # Split this up
    sortFields = [s for s in sortValue.split(',')]
    
    orderByFlds = []
    # Split this up again and build a list to provide to the order_by method as an args list.
    # Each sortFld should look like this: <fieldName>;<direction>. Eg: 'title;-1' or 'title;-1'
    for sortFld in sortFields:
        # Get the direction (ascending or descending)
        fld, direction = sortFld.split(';')
        if int(direction) == -1:
            fld = "-" + fld
        
        orderByFlds.append(fld)
        print orderByFlds
        
    # Sort the results
    try:
        resultSet = resultSet.order_by(*orderByFlds)
    except:
        logging.error('Failed on field sorting. Fields/Values-- %s'%sortValue)
        resultSet = None
        
    return resultSet

#------------------------------------------------------------------------

def filteredRetrieval(projectsModel, params):
    ''' Gets the db objects filtered on content '''
    
    # Get all of the results with only the fields we want
    resultSet = projectModel.objects.all()
    
    # TAGS FILTERING
    if settings.TAG_URL_KEY_NAME in params.keys():
        resultSet = tagBasedFilter(resultSet, params) 


    # FILTERING
    validFlds = settings.VALID_FILTER_FIELDS
    paramFlds = params.keys() 
    # Are any of the URL parameter fields in the list of valid filter fields?
    # An empty list evaluates to False.
    if bool([i for i in validFlds if i in paramFlds]) == True:
        resultSet = exactMatchFilter(resultSet, params)


    # MULTI-FIELD SORTING
    if settings.SORT_URL_KEY_NAME in params.keys():
        resultSet = sortedResults(resultSet, params)





