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
            idea.title = cleanForm['title']
            idea.desciption  = cleanForm['description']
            idea.classification = cleanForm['cls']
            '''
            idea_headers = formatHttpHeaders(headers)
            res = saveIdea(cleanForm['title'],cleanForm['description'],cleanForm['cls'], idea_headers)
            #idea.email_starter = formatSubmitterEmail(user)
            # For the output page
            c['title'] = idea.title
            c["description"] = idea.description
            c['classification'] = idea.classification
                
            return render_to_response('ideasapp/idea_thanks.html', c)
    
        else:
            logging.error("User failed to enter valid content into form.")
            c['form'] = form
            return render_to_response("ideasapp/idea_submit.html", c)
        
    else:
        form = ideaForm()
        c.update({"form":form})
    
    return render_to_response("ideasapp/idea_submit.html", c)
#-------------------------------------------------------------------#        

def ideas_cloud(request):
    #import pdb
    #pdb.set_trace()
    ''' Renders a word cloud of ideas '''
    c = {"classification":"unclassified",
         "page_title":"Recent Ideas"}
    c.update(csrf(request))
    ideasData = ideasCloud('pub_date')
    outData = []
    for i in ideasData:
        outData.append(str(i[0]))
    c['ideas']=outData
    
    return render_to_response("ideasapp/ideas_cloud.html", c)
            
#-------------------------------------------------------------------#   

def back(idea_id):
    '''The back this idea link was clicked somewhere'''
    return idea_id
    #TODO: Finish off this functionality!

#-------------------------------------------------------------------#  
        
def ideas_list(request):     
    c = {"classification":"unclassified",
         "page_title":"All Ideas"}
    c.update(csrf(request))
    pData = ideaModel.objects.values_list('title','description','pub_date', 'num_backers')
    c['headings']=['Idea Title','Date Published','Idea Detail','Number of Backers']
    c['tableData'] = pData
    
    return render_to_response("ideasapp/ideas_list.html", c)
            
#-------------------------------------------------------------------#  
def ideas_all(request):
    #Use if all data from table is needed into a dynamic table
    c = {"classification":"unclassified",
         "page_title":"All Ideas"}
    c.update(csrf(request))
    #Use if all data from table is needed into a dynamic table
    data = ideaModel.objects.all()
    #Get the field names
    headers = data.values()[0].keys()
    #ToDO: Make them prettier
    #headersOut = []
    c['headings']= headers
    #Get table data
    row = []
    rows = []
    for r in data.values():
        for field in headers:
            #Get the user from the header as an example
            if field == 'headers':
                row.append('header_info_tbc')
            else: row.append(r[field])
        rows.append(row)
        row = []
    del row
    del data
    rows.append('Back')
    c['tableData'] = rows

    return render_to_response("ideasapp/ideas_list.html", c)
            
#-------------------------------------------------------------------#               
            
            
            
            
            
            
            
            
            
