from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.core.context_processors import csrf

import os
import sys
import logging
import hashlib
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
from code import saveTags, distinctTagsSortedAlpha

logging.getLogger(__name__)

#------------------------------------------------------------------------------------

def submit(request):
    ''' Contact form rendering & submission. '''

    c = {"classification":"unclassified",
         "page_title":"Share your idea"}
    
    c.update(csrf(request))

    # Create the tag list for selecting by user
    c['known_tags'] = distinctTagsSortedAlpha()
    
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
            savedIdea = saveIdea(cleanForm['title'],cleanForm['description'],cleanForm['cls'], idea_headers)
            
            # We can only add tags to a saved object - this saves the structured ones
            res = saveTags(savedIdea, cleanForm['new_tags'])
            
            # This saves the unstructured ones
            res = saveTags(savedIdea, cleanForm['existing_tags'])
            
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

    #Template for model outputs
    template_headings = [{'db':'title', 'pretty':'Idea Title'}, 
                         {'db':'pub_date', 'pretty':'Date Published'},
                        {'db':'description', 'pretty':'Idea Description'},
                        {'db':'num_backers', 'pretty':'Number of Backers'}]
    #get the values form db - this could be user requested - e.g. based on pub date
    pData = ideaModel.objects.values_list('title','pub_date','description', 'num_backers')
    #Make the pretty headings
    #c['headings']=['Idea Title','Date Published','Idea Detail','Number of Backers']
    #Instantiate our out vars
    out = []
    outrow = {'uid':'','cells':[]}
    celldict = {'field':'','full':'','short':'','id':''}
    for pDataidx, row in enumerate(pData):
        for headingidx, heading in enumerate(template_headings):
            celldict['field']=heading['pretty']
            '''
            #TODO: alter this to search for specific data types
            if heading['db']=='idea_text' and ideaModel._meta.get_field(heading['db']).get_internal_type() == 'CharField' and len(row[headingidx])>200:
                rowdict['short']=row[headingidx][:200]
                rowdict['full']=row[headingidx][200:]
            else: 
                rowdict['short']=''
            '''
            celldict['full']=row[headingidx]
            celldict['id']='idea'+str(pDataidx)+str(headingidx)
            outrow['cells'].append(celldict.copy())
        #Do a hash of the title to store as uid
        uid = hashlib.sha1(row[0]).digest()
        outrow['uid']=uid
        out.append(outrow.copy())
        outrow = {'uid':'','cells':[]}
    c['headings'] = template_headings      
    c['tableData'] = out
    
    return render_to_response("ideasapp/ideas_list.html", c)
            
#-------------------------------------------------------------------#               
            
def like(request,ideaid):
    ''' Liking and disliking. '''
    
    #Databases clicks of the like and dislike buttons
    # Has the form been submitted?
    if request.method == 'GET': 
        #dislike_ideas183
        #Strip the choice
        print ideaid
        return HttpResponse(str(ideaid))
            
            
            
            
            
            
            
