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
    print params
    # Get the field user has requested to sort on
    sortValue = params[settings.SORT_URL_KEY_NAME]
    
    # sortValue should look like this: "<fieldName1>;<direction>,<fieldName2>;<direction>"
    # Split this up
    orderByFlds = [s for s in sortValue.split(',')]
            
    # Sort the results
    try:
        resultSet = resultSet.order_by(*orderByFlds)
    except:
        logging.error('Failed on field sorting. Fields/Values-- %s'%sortValue)
        resultSet = None
        
    return resultSet

#------------------------------------------------------------------------

def filteredRetrieval(targetModel, params):
    ''' Gets the db objects filtered on content '''
    
    # Get all of the results with only the fields we want
    resultSet = targetModel.objects.all()
    
    # TAGS FILTERING
    if settings.TAG_URL_KEY_NAME in params.keys():
        resultSet = tagBasedFilter(resultSet, params)
    
    # FILTERING
    validFlds = settings.VALID_FILTERS
    paramFlds = params.keys()
     
    # Are any of the URL parameter fields in the list of valid filter fields?
    # An empty list evaluates to False.
    if bool([i for i in validFlds if i in paramFlds]) == True:
        resultSet = exactMatchFilter(resultSet, params)

    # MULTI-FIELD SORTING
    if settings.SORT_URL_KEY_NAME in params.keys():
        resultSet = sortedResults(resultSet, params)
    

    return resultSet

#------------------------------------------------------------------------

def buildSingleSortUrl(key, reverse=False):
    ''' Builds the url to be called for sorting '''

    if reverse == True:
        url = '?%s=-%s' %(settings.SORT_URL_KEY_NAME, key)
    else:
        url = '?%s=%s' %(settings.SORT_URL_KEY_NAME, key)
    return url

#------------------------------------------------------------------------

def buildSingleFieldFilterUrl():
    ''' Builds the url to be called for field-based filtering '''

    # This to probably be handled in js because it needs user text input

#------------------------------------------------------------------------

def buildSingleTagFilterUrl():
    ''' Builds the url to be called for tag-based filtering '''
    
    return "?%s=" %settings.TAG_URL_KEY_NAME
    
#------------------------------------------------------------------------

def buildSingleSortAndFilterItems():
    ''' Builds all the sort and filter items including urls and pretty names '''

 
    sortItems = []
    # SORT capable fields
    for key, val in settings.VALID_SORT_FIELDS.items():

        # For positive sorts
        li = {'url'          : buildSingleSortUrl(key),
              'display_name' : val,
              'direction'    : 0,
              'id'           : "%s" %(key)}
        sortItems.append(li)
        # For negative sorts
        """
        li = {'url'          : buildSingleSortUrl(key, reverse=True),
              'display_name' : val + '(desc)',
              'id'           : "%s_desc" %(key)}
        sortItems.append(li)
        """
        
    # Tag item
    tagItem = {'url'          : buildSingleTagFilterUrl(),
               'display_name' : 'Filter',
               'id'           : 'tag_filter'}
    
    return {"tag_item" : tagItem,
            "sort_items" : sortItems}
               
    






