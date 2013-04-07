import re
import ideasapp.settings as settings
from ideasapp.models import idea as ideaModel
from datetime import datetime

def formatHttpHeaders(headers):
    ''' formats http headers into a nasty long string because we're not using a document store
        NOT TESTED'''
    
    out = ""
    
    for key in headers.keys():
        out += "%s:%s;" %(key, headers[key])
    
    out.rstrip(";")
    
    return out

#------------------------------------------------------------------------------------------

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

def ideasCloud():
    ''' Gets all ideas from db and returns them for rendering with some measure of how to render 
    Initially this rendering will be based on classification - higher class = bigger font'''
    #import pdb
    #pdb.set_trace()  
    data = ideaModel.objects.all()
    #data here is a list of dictionaries
    return data
#------------------------------------------------------------------------------------------
def getDate():
    return datetime.now()

#------------------------------------------------------------------------------------------
def saveIdea(ideaTitle, ideaText, ideaClassification, ideaHeaders):
    ''' Processes idea form data and saves data '''
    #import pdb
    #pdb.set_trace()    
    out = ideaModel(idea_title = ideaTitle, pub_date = getDate(), idea_text = ideaText, num_backers = 1, idea_classification = ideaClassification, idea_headers = ideaHeaders)
    out.save()
    return 
#------------------------------------------------------------------------------------------

        
    






