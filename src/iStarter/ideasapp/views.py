from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.core.context_processors import csrf

import os
import sys
import logging
import hashlib
import base64
from datetime import datetime
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
from projectsapp.models import project as projectModel
from ideasapp.models import ideaLikes as likesModel
from code import formatSubmitterEmail, formatHttpHeaders, ideasCloud, getDate, saveIdea
from code import saveTags, distinctTagsSortedAlpha
from django.db.models import Avg, Max

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
        
def ideas_list(request):     
    c = {"classification":"unclassified",
         "page_title":"All Ideas"}
    c.update(csrf(request))

    #Template for model outputs
    template_headings = [{'db':'title', 'pretty':'Idea Title'}, 
                         {'db':'pub_date', 'pretty':'Date Published'},
                         {'db':'description', 'pretty':'Idea Description'},
                            {'db':'linked_projects','pretty':'Linked Projects'},
                            {'db':'response', 'pretty':'Responses'}
                            ]
    
    pData = ideaModel.objects.values_list('title','pub_date','description', 'likes', 'dislikes','pk', 'id')
    max_likes = ideaModel.objects.all().aggregate(Max('likes'))
    max_dislikes = ideaModel.objects.all().aggregate(Max('dislikes'))
    out = []
    outdict = {'title':'','pub_date':'','description':'','likes':0,'dislikes':0, 'perc_likes':0,'perc_dislikes':0, 'linked_projects':[]}
    for row in pData:
        outdict['title']=row[0]
        outdict['pub_date']=row[1]
        outdict['description']=row[2]
        outdict['likes']=int(row[3])
        outdict['dislikes']=int(row[4])
        outdict['perc_likes']=100*outdict['likes']/max_likes['likes__max']
        outdict['perc_dislikes']=100*outdict['dislikes']/max_dislikes['dislikes__max']
        outdict['id'] = row[6]
        projs = projectModel.objects.filter(ideas_derived_from=row[5])
        if projs:
            for proj in projs:
                outdict['linked_projects'].append(proj.id)
        out.append(outdict.copy())
        print outdict
        outdict['linked_projects']=[]
        
    c['headings'] = template_headings
    c['tableData'] = out
    
    return render_to_response("ideasapp/ideas_list.html", c)            

    '''
    #get the values form db - this could be user requested - e.g. based on pub date
    pData = ideaModel.objects.values_list('title','pub_date','description', 'likes', 'dislikes')
    #Make the pretty headings
    #c['headings']=['Idea Title','Date Published','Idea Detail','Number of Backers']
    #Instantiate our out vars
    out = []
    outrow = {'uid':'','cells':[]}
    celldict = {'field':'','full':'','short':'','id':''}
    for pDataidx, row in enumerate(pData):
        for headingidx, heading in enumerate(template_headings):
            celldict['field']=heading['pretty']
            if heading['db']=='likes' or heading['db']=='dislikes':
                celldict['full']=int(row[headingidx])
            else:
                celldict['full']=row[headingidx]
            #This is the autogenerated id we'll use in the tempalte
            celldict['id']='idea'+str(pDataidx)+str(headingidx)
            outrow['cells'].append(celldict.copy())
        #Do a hash of the title to store as uid
        uid = base64.b64encode(hashlib.sha256(row[0]).digest(), altchars="ZZ")[:32]
        outrow['uid']=uid
        out.append(outrow.copy())
        outrow = {'uid':'','cells':[]}
    c['headings'] = template_headings      
    c['tableData'] = out
    
    return render_to_response("ideasapp/ideas_list.html", c)
'''

#-------------------------------------------------------------------#               

def unlike(request, ideaid):
    ''' This is the reverse of clicking on a selected like/dislike button '''
    if request.method == 'GET': 
        #dislike_ideas183
        #Strip the choice
        idea_id = ideaid[ideaid.find('_')+1:]

        choice = ideaid[:ideaid.find('_')]

        #Now record this in the db

        if choice in ['like', 'dislike']:
 
            #Now record this in the db
            iData = ideaModel.objects.filter(id=idea_id)[0]
            oldLike = likesModel.objects.filter(title=iData, vote_type = choice).order_by('vote_date')[0]
            print 'Found one at', oldLike.vote_date
            if choice == 'like':
                iData.likes -= 1
                newVal = iData.likes
                
            elif choice == 'dislike':
                iData.dislikes -= 1
                newVal = iData.dislikes
                
            xml = '<xml><data><iddata>'+str(int(newVal))+'</iddata><valdata>'+str(idea_id)+'</valdata></data></xml>'
            iData.save()
            oldLike.delete()
        else:
            xml = '<xml><error>Invalid choice "' + choice + '" selected</error></xml>'
        return HttpResponse(xml, content_type="text/xml")
    
def like(request,ideaid):
    ''' Liking and disliking. '''
    
    #Databases clicks of the like and dislike buttons
    # Has the form been submitted?
    if request.method == 'GET': 
        #dislike_ideas183
        #Strip the choice
        idea_id = ideaid[ideaid.find('_')+1:]

        choice = ideaid[:ideaid.find('_')]

        #Now record this in the db

        if choice in ['like', 'dislike']:
 
            #Now record this in the db
            iData = ideaModel.objects.filter(id=idea_id)[0]
            newLike = likesModel(title=iData, vote_date=datetime.now(), vote_type = choice)

            if choice == 'like':
                iData.likes += 1
                newVal = iData.likes
                
            elif choice == 'dislike':
                iData.dislikes += 1
                newVal = iData.dislikes
                
            xml = '<xml><data><iddata>'+str(int(newVal))+'</iddata><valdata>'+str(idea_id)+'</valdata></data></xml>'
            iData.save()
            newLike.save()
        else:
            xml = '<xml><error>Invalid choice "' + choice + '" selected</error></xml>'
        return HttpResponse(xml, content_type="text/xml")
            
#-------------------------------------------------------------------#              

def ideas_gallery(request):
    ''' Display all the projects as table list of icons'''
    c = {"classification":"unclassified","page_title":"iStarter Ideas Gallery"}
    c.update(csrf(request))
    pData = ideaModel.objects.values_list('title','pub_date','description', 'pk', 'likes', 'dislikes')
    '''
    #Get the average for likes and dislikes
    avg_likes = ideaModel.objects.all().aggregate(Avg('likes'))
    print avg_likes
    avg_dislikes = ideaModel.objects.all().aggregate(Avg('dislikes'))
    print avg_dislikes
    '''
    max_likes = ideaModel.objects.all().aggregate(Max('likes'))
    #print max_likes
    max_dislikes = ideaModel.objects.all().aggregate(Max('dislikes'))
    #print max_dislikes
    rowdict = {'title':'','pub_date':'','description':'','id':'','likes':'','dislikes': ''}

    #Template for model outputs
    template_headings = [{'db':'title', 'pretty':'Idea Title'}, 
                         {'db':'pub_date', 'pretty':'Date Published'},
                        {'db':'description', 'pretty':'Idea Description'},
                        {'db':'pk','pretty':'Project Id'},
                        {'db':'likes', 'pretty':'Likes'},
                        {'db':'dislikes', 'pretty':'Disikes'},
                        ]

    # Prepare the data to pass to the HTML
    #outrow = []
    out = []
    outrow = {'uid':'','perc_likes':'','perc_dislikes':'','cells':[]}
    for pDataidx, row in enumerate(pData):
        for headingidx, heading in enumerate(template_headings):
            if heading['db']=='title' :
                rowdict['title'] = row[headingidx][:20]
            if heading['db']=='pub_date' :
                rowdict['pub_date'] = row[headingidx]
            if heading['db']=='description' :
                rowdict['description'] = row[headingidx][:100]
            if heading['db']=='pk':
                rowdict['id']=row[headingidx]
            if heading['db']=='likes':
                rowdict['likes']=int(row[headingidx])
            if heading['db']=='dislikes':
                rowdict['dislikes']=int(row[headingidx])
        outrow['cells'].append(rowdict.copy())
        outrow['perc_likes']=100*rowdict['likes']/max_likes['likes__max']
        outrow['perc_dislikes']=100*rowdict['dislikes']/max_dislikes['dislikes__max']
        outrow['uid']=str(rowdict['id'])
        out.append(outrow.copy())
        outrow = {'average_likes':'','average_dislikes':'','cells':[]}
    c['tableData'] = out
    c['headings'] = template_headings
	
    return render_to_response("ideasapp/ideas_gallery.html", c)	          
            
            
            
            
