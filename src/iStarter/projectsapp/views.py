from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.db.models import Count, Min, Sum, Max, Avg
from django.http import HttpResponse, Http404

import os
import sys
import logging
from datetime import datetime
import collections

from random import randint
import hashlib
import base64

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

from projectsapp.models import project as projectModel
from projectsapp.models import pvote as projectVoteModel

from ideasapp.models import idea as ideaModel

from projectsapp.forms import projectForm
from projectsapp.forms import backForm
from code import formatSubmitterEmail, formatHttpHeaders, getDate, saveProject
from code import saveTags, distinctTagsSortedAlpha

def submit(request):
    ''' Pulling together ideas into a glorious project. '''

    c = {"classification":"unclassified",
         "page_title":"Submit a Project"}
    c.update(csrf(request))
    
    # Create the tag list for selecting by user
    c['known_tags'] = distinctTagsSortedAlpha()
    
    # Has the form been submitted?
    if request.method == 'POST':
        
        form = projectForm(request.POST)
        
        if form.is_valid():

            # Instantiate an idea
            project = projectModel()

            # Proper Header and django-based user
            headers = request.META
            #user = str(request.user)
            
            # Form content extracted            
            cleanForm = form.cleaned_data

            project_headers = formatHttpHeaders(headers)

            savedProject = saveProject(cleanForm['title'],
                                       cleanForm['description'],
                                       cleanForm['cls'],
                                       cleanForm['ideas'],
                                       project_headers,
                                       cleanForm['importance_level'],
                                       cleanForm['effort_level'],
                                       cleanForm['resource_level']
                                       )
                                    
            # We can only add tags to a saved object - this saves the structured ones
            res = saveTags(savedProject, cleanForm['new_tags'])
            
            # This saves the unstructured ones
            res = saveTags(savedProject, cleanForm['existing_tags'])

            #idea.email_starter = formatSubmitterEmail(user)
            # For the output page
            c['title'] = project.title
            c["description"] = project.description
            c['classification'] = project.classification
            
            return render_to_response('projectsapp/project_thanks.html', c)
    
        else:
            logging.error("User failed to enter valid content into form.")
            c['form'] = form
            return render_to_response("projectsapp/project_submit.html", c)
        
    else:
        form = projectForm()
        c.update({"form": form})

    return render_to_response('projectsapp/project_submit.html', c)

def project_list(request):     
    c = {"classification":"unclassified",
         "page_title":"All Projects"}
    c.update(csrf(request))

    #pData = projectModel.objects.annotate(likes = Sum('pvote__like'), backs = Sum('pvote__backer')).order_by('-pub_date').values('id','title','description','pub_date')
    pData = projectModel.objects.order_by('-pub_date').values('id','title','description','pub_date',
                                                               'num_likes', 'num_dislikes', 'num_backers')
    c['headings']=['Project Title','Project Description', 'Date Published', 'Likes', 'Dislikes', 'Backers', 'Vote', 'Back']
    c['tableData'] = pData

    return render_to_response("projectsapp/project_list.html", c)
            	
def like(request, projectid):
    ''' Liking and disliking. '''
    
    #Databases clicks of the like and dislike buttons
    # Has the form been submitted?

    if request.method == 'GET': 
        
        # Parse the projectid
        splt = projectid.split('_')
        
        prjid = splt[1]
        choice = splt[0]
 
        if choice in ['like', 'dislike', 'back']:
 
            #Now record this in the db
            pData = projectModel.objects.filter(id=prjid)[0]
            newLike = projectVoteModel(project=pData, vote_date=datetime.now(), vote_type = choice)

            if choice == 'like':
                pData.num_likes += 1
                newVal = pData.num_likes
                
            elif choice == 'dislike':
                pData.num_dislikes += 1
                newVal = pData.num_dislikes
                
            elif choice == 'back':
                pData.num_backers +=1
                newVal = pData.num_backers
                
            xml = '<xml><data><iddata>'+str(int(newVal))+'</iddata><valdata>cell'+str(choice)+'_'+prjid+'</valdata></data></xml>'
            pData.save()
            newLike.save()

        return HttpResponse(xml, content_type="text/xml")
    
def project_gallery(request):
	''' Display all the projects as table list of icons'''
	c = {"classification":"unclassified","page_title":"iSTARter Project Gallery"}
	c.update(csrf(request))
	pData = projectModel.objects.values_list('title','pub_date','description', 'num_backers', 'pk', 'importance', 'effort', 'resource', 'projActive', 'num_likes', 'num_dislikes')
	rowdict = {'title':'','pub_date':'','description':'','backPercentage':'','id':'', 'importance':'', 'effort':'', 'resource':'', 'projActive':'', 'num_likes':'', 'num_dislikes':''}

 	#Template for model outputs
 	template_headings = [{'db':'title', 'pretty':'Idea Title'}, 
                         {'db':'pub_date', 'pretty':'Date Published'},
                        {'db':'description', 'pretty':'Idea Description'},
                        {'db':'num_backers', 'pretty':'Number of Backers'},
                        {'db':'pk','pretty':'Project Id'},
						{'db':'importance','pretty':'Importance of task'},
                        {'db':'effort','pretty':'Level of Effort required'},
                        {'db':'resource','pretty':'Resources required'},
                        {'db':'projActive','pretty':'Project is Active'},
                        {'db':'num_likes','pretty':'Number of Likes'},
                        {'db':'num_dislikes','pretty':'Number of Dislikes'}]
	
	# First find maximum backers todate
	maxbackers= -1
	backers=0
	for pDataidx, row in enumerate(pData):
		for headingidx, heading in enumerate(template_headings):
			if heading['db']=='num_backers' :
				backers=row[headingidx]
			if backers > maxbackers :
				maxbackers=backers

	# Sometime need to do it this way instead of the loop
	# dont know how yet though
	# maxbackers = projectModel.objects.annotate(likes = Max('num_backers'))

	# Prepare the data to pass to the HTML
	outrow = []
	out = []

	for pDataidx, row in enumerate(pData):
		for headingidx, heading in enumerate(template_headings):
			if heading['db']=='title' :
				rowdict['title'] = row[headingidx][:20]
			if heading['db']=='pub_date' :
				rowdict['pub_date'] = row[headingidx]
			if heading['db']=='description' :
				rowdict['description'] = row[headingidx][:200]
			if heading['db']=='num_backers' :
				rowdict['backPercentage'] = 100 * row[headingidx] / maxbackers
			if heading['db']=='pk':
				rowdict['id']=row[headingidx]
			if heading['db']=='importance' :
				rowdict['importance']=row[headingidx]
			if heading['db']=='effort' :
				rowdict['effort']=row[headingidx]
			if heading['db']=='resource' :
				rowdict['resource']=row[headingidx]
			if heading['db']=='projActive' :
				if pDataidx == 2 or pDataidx==4 :
					rowdict['projActive']= 1 # row[headingidx]
				else:
					rowdict['projActive']= 0 # row[headingidx]
			if heading['db']=='num_likes' :
				rowdict['num_likes']=int(row[headingidx])
			if heading['db']=='num_dislikes' :
				rowdict['num_dislikes']=int(row[headingidx])				
        	outrow.append(rowdict.copy())
		out.append(outrow)
		outrow = []
	c['tableData'] = out
	c['headings'] = template_headings
	
	return render_to_response("projectsapp/project_gallery.html", c)	
 
def project_detail(request,projid):
    ''' Display detail on a project '''
    
    #Select the project from table
    outData = projectModel.objects.get(pk=int(projid))
    rowdict = {'title':'','pub_date':'','description':'','num_backers':'','id':'','backPercentage':''}
    
    #Template for model outputs
    template_headings = [{'db':'title', 'pretty':'Idea Title'}, 
                         {'db':'pub_date', 'pretty':'Date Published'},
                        {'db':'description', 'pretty':'Idea Description'},
                        {'db':'num_backers', 'pretty':'Number of Backers'}]

    #Prepare the data to pass to the HTML
    #rowdict['title'] = outData.title
    rowdict['pub_date'] = outData.pub_date
    rowdict['description'] = outData.description
    rowdict['num_backers'] = outData.num_backers
    rowdict['id']=projid
    maxbackers= -1
    backers = outData.num_backers
    if backers > maxbackers:
        maxbackers=backers
    rowdict['backPercentage'] = 100 * randint(0,backers) / maxbackers
    c = {"classification":"unclassified","page_title":outData.title}
    c.update(csrf(request))
    c['data'] = rowdict
    c['headings'] = template_headings    
    
    ''' Here on down is the code for making related ideas table '''    
    
     #Template for model outputs
    template_headings_ideas = [{'db':'title', 'pretty':'Idea Title'}, 
                         {'db':'pub_date', 'pretty':'Date Published'},
                         {'db':'description', 'pretty':'Idea Description'},
                         {'db':'likes', 'pretty':'Number of Likes'},
                         {'db':'dislikes', 'pretty':'Number of DisLikes'}]
    #get the values form db - this could be user requested - e.g. based on pub date
    pideaData = outData.ideas_derived_from.values_list('title','pub_date','description','likes','dislikes')
    out = []
    outrow = {'uid':'','cells':[]}
    celldict = {'field':'','full':'','short':'','id':''}
    for pDataidx, row in enumerate(pideaData):
        for headingidx, heading in enumerate(template_headings_ideas):
            #print row[headingidx]
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
    c['headings_ideas'] = template_headings_ideas      
    c['tableData_ideas'] = out
    print out

    return render_to_response("projectsapp/project_detail.html", c)


def back(request, projid):
    ''' Backing a project '''

    c = {"classification":"unclassified",
         "page_title":"Back Project:"}
    c.update(csrf(request))
    # Has the form been submitted?
    if request.method == 'POST':
        
        form = backForm(request.POST)
        
        if form.is_valid():

            # Proper Header and django-based user
            headers = request.META
            #user = str(request.user)
            
            # Form content extracted            
            cleanForm = form.cleaned_data
            #project_headers = formatHttpHeaders(headers)

            #res = saveProject(cleanForm['title'], cleanForm['description'], cleanForm['cls'], cleanForm['ideas'], project_headers)
            #idea.email_starter = formatSubmitterEmail(user)
            if projectModel.objects.filter(pk=projid).count() != 0:
                outBack = projectModel.objects.get(pk=projid)
                outBack.num_backers=outBack.num_backers+1
                outBack.save()
                outPvote = projectVoteModel()
                outPvote.project_id=projid
                outPvote.vote_date =datetime.now()
                outPvote.vote_type='back'
                outPvote.support_type=cleanForm['support']
                outPvote.classification=cleanForm['cls']
                outPvote.save()
                #outPvote = projectVoteModel(project=projid,vote_date=datetime.now(),vote_type='back',support_type=cleanForm['support'],
                                            #classification=cleanForm['cls'])
                outPvote.save()
                # For the output page
                c['title'] = outBack.title
                c['support'] = outPvote.support_type
                #c["description"] = outBack.description
                c['classification'] = outBack.classification
                
                return render_to_response('projectsapp/project_thanks.html', c)
                
            else:
                logging.error("User tried to back a project that didnt exist")
                outData = projectModel.objects.get(pk=int(projid))
                c['form'] = form
                c['title']=outData.title
                return render_to_response("projectsapp/project_back_submit.html", c)
    
        else:
            logging.error("User failed to enter valid content into form.")
            outData = projectModel.objects.get(pk=int(projid))
            c['form'] = form
            c['title']=outData.title
            return render_to_response("projectsapp/project_back_submit.html", c)
        
    else:
        if projectModel.objects.filter(pk=projid).count() != 0:
            #get Title from projid
            outData = projectModel.objects.get(pk=int(projid))
            form = backForm()
            c.update({"form": form})
            c.update({'title':outData.title})
            return render_to_response('projectsapp/project_back_submit.html', c)
        else:
            raise Http404

