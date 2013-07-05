import re
import operator
import ideasapp.settings as settings
from projectsapp.models import project as projectModel
import logging

import sys
sys.path.append('..')
from ideasapp.models import idea as ideaModel

from datetime import datetime

logging.getLogger(__name__)

def formatHttpHeaders(headers):
    ''' formats http headers into a nasty long string because we're not using a document store
        NOT TESTED'''
    
    out = ""
    
    for key in headers.keys():
        out += "%s:%s;" %(key, headers[key])
    
    out.rstrip(";")
    
    return out
#
#------------------------------------------------------------------------------------------

## This needs to be moved to be shared between apps
def formatSubmitterEmail(user):
    ''' Checks whether the submitter's id is an email. If not appends a domain to it
        NOT TESTED'''

    # Email regex
    regex = re.compile(r"^([A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*)$")
    regOut = re.match(regex, user)

    if regOut:
        email = regOut.group(0)

    # J number regex
    regex = re.compile(r'^([a-zA-Z]\d{5})$')
    regOut = re.match(regex, user)

    if regOut:
        jNumber = regOut.group(1)
        email = jNumber + '@' + settings.emailDomain 
    else:
        email = None
        
    return email

#------------------------------------------------------------------------------------------
#
#def ideasCloud(order):
#    ''' Gets all ideas from db and returns them for rendering with some measure of how to render 
#    Initially this rendering will be based on classification - higher class = bigger font'''
#    #Pardsed in var in the field to order by for changing font
#
#    #data = ideaModel.objects.order_by(order).values_list('idea_title', 'pub_date')
#    #data = ideaModel.objects.values_list('idea_title', 'pub_date')
#    data = ideaModel.objects.order_by(order).values_list('idea_title', 'pub_date')
#    
#    return data
#------------------------------------------------------------------------------------------
def getDate():
    return datetime.now()

#------------------------------------------------------------------------------------------
def saveProject(title, description, classification, ideas, headers, importance_level, effort_level, resource_level):
    ''' Processes idea form data and saves data '''
    #import pdb
    #pdb.set_trace()    
    out = projectModel(title = title, pub_date = getDate(), description = description,
                       classification = classification, headers = headers, 
                       num_backers=1, num_likes=1, num_dislikes=0,
                       importance=importance_level, effort=effort_level, resource=resource_level)

    out.save()
    for idea in ideas:
        idObj = ideaModel.objects.get(id=idea)
        out.ideas_derived_from.add(idObj)
        
    return out

#------------------------------------------------------------------------------------------
def saveTags(target, tags):
    '''Saves the tags to the idea'''
    
    for t in tags:
        target.tags.add(t)
    target.save()
    return target

#------------------------------------------------------------------------

def distinctTagsSortedAlpha():
    ''' Get a distinct list of tags from the db '''
    
    tags = projectModel.tags.all().distinct()
    outTags = [str(t) for t in tags]
    outTags.sort()
    
    return outTags

#------------------------------------------------------------------------

def distinctTagsSortedCount(reverse=True):
    ''' Get a list of tags sorted by frequency and by alphabetical order. '''
    
    outTagsDict = {}
    
    res = projectModel.objects.all()
    for row in res:
        tags = row.tags.values()
        for tag in tags:
            try:
                outTagsDict[tag['name']] += 1
            except:
                outTagsDict[tag['name']] = 1
    
    outTagsList = [[key, val] for key, val in outTagsDict.iteritems()]
    # First up, sort by the SECONDARY KEY
    outTagsList.sort(key=operator.itemgetter(0))
    # Now sort by the PRIMARY KEY, which is count
    outTagsList.sort(key=operator.itemgetter(1), reverse=reverse)
    
    return outTagsList
    
#------------------------------------------------------------------------
# code to calculate the numbr of backers required before a project is taken on
#
#	effort 		: The amount of effort required to complete the project (1-5)
#		It might require a lot of software design, or development of a new algorithm
#				This is really a measure of manpower requirements
#   importance 	: How important is it that the project gets taken on (1-5)
# 		This could reflect the national priority framework or it might be 
#		that other initiatives cannot be taken on until this is completed
#	resources	: How many extra resources are required to achived the projects goals (1-5)
#		This are things that cost money Examples are: needs a new computer; needs 
# 		software purchasing; needs new paperclips
#
def backersRequiredAlgorithm(effort, importance, resources) :		
	return effort * ((6-importance)**2) * (resources**3)

#------------------------------------------------------------------------

def getMaxClassification(results):
    ''' Gets the maximum classification of the objects returned. '''

    classificationRank = [c[0].lower() for c in settings.CLASSIFICATIONS]
    
    maxClass = classificationRank[-1]
    maxClassIdx = 0
    if len(results) == 0:
        maxClass = 'unclassified'
    
    # Get the results
    for res in results:
        
        try:
            cls = res.classification.lower()
        except:
            continue
        
        # Ensure it matches our known set, get it's index in the ranked scale
        if cls in classificationRank:
            classIdx = classificationRank.index(cls)
            
            # If it's higher than the highest so far, reset the highest so far
            if classIdx > maxClassIdx:
                maxClassIdx = classIdx
                maxClass    = cls
        
    return maxClass    
    
    
