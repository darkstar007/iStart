from django.shortcuts import render_to_response
from django.core.context_processors import csrf

import os
import sys
import logging
#============================================================================================
# TO ENSURE ALL OF THE FILES CAN SEE ONE ANOTHER.

appRoot = os.path.dirname(os.path.realpath(__name__))

# Find out whats in this directory recursively
for root, subFolders, files in os.walk(appRoot):
    # Loop the folders listed in this directory
    for folder in subFolders:
        directory = os.path.join(root, folder)
        if directory.find('.git') == -1:
            if directory not in sys.path:
                sys.path.append(directory)

#============================================================================================

#FOSS
from ideasapp.forms import ideaForm
from ideasapp.models import idea as ideaModel
from code import formatSubmitterEmail, formatHttpHeaders, ideasCloud, getDate, saveIdea

logging.getLogger(__name__)

#------------------------------------------------------------------------------------

def submit(request):
    ''' Contact form rendering & submission. '''

    c = {"classification":"unclassified",
         "page_title":"Share your idea"}
    
    c.update(csrf(request))

    # Has the form been submitted?
    if request.method == 'POST':
        
        form = ideaForm(request.POST)
        
        if form.is_valid():

            # Instantiate an idea
            idea = ideaModel()

            # Proper Header and django-based user
            headers = request.META
            #user = str(request.user)
            
            # Form content extracted            
            cleanForm = form.cleaned_data
            '''
            idea.idea_title = cleanForm['title']
            idea.idea_text  = cleanForm['description']
            idea.idea_classification = cleanForm['cls']
            '''
            idea_headers = formatHttpHeaders(headers)
            res = saveIdea(cleanForm['title'],cleanForm['description'],cleanForm['cls'], idea_headers)
            #idea.email_starter = formatSubmitterEmail(user)
            # For the output page
            c['title'] = idea.idea_title
            c["description"] = idea.idea_text
            c['classification'] = idea.idea_classification
                
            return render_to_response('ideasapp/idea_thanks.html', c)
    
        else:
            logging.error("User failed to enter valid content into form.")
            c['form'] = form
            return render_to_response("ideasapp/idea_submit.html", c)
        
    else:
        form = ideaForm()
        c.update({"form":form})
    
    return render_to_response("ideasapp/idea_submit.html", c)
     

def ideas_cloud(request):
    #import pdb
    #pdb.set_trace()
    ''' Renders a word cloud of ideas '''
    c = {"classification":"unclassified",
         "page_title":"Recent Ideas"}
    
    c.update(csrf(request))
    
    ideasData = ideasCloud()
    c['ideas']=ideasData
    
    return render_to_response("ideasapp/ideas_cloud.html", c)
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            