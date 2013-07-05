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

import projectsapp.settings as settings
from projectsapp.code import getMaxClassification

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
from customObjectQueries import filteredRetrieval, validateQueryParams, buildSingleSortAndFilterItems
from code import backersRequiredAlgorithm
from projectScoringAlgs import backersRequiredAlgorithm as brAlg

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

def unlike(request, projectid):
    ''' This is the reverse of clicking on a selected like/dislike button '''
    if request.method == 'GET': 

        # Parse the projectid
        splt = projectid.split('_')
        
        prjid = splt[1]
        choice = splt[0]

        #Now record this in the db

        if choice in ['like', 'dislike']:
 
            #Now record this in the db
            pData = projectModel.objects.filter(id=prjid)[0]
            oldLike = projectVoteModel.objects.filter(project=pData, vote_type = choice).order_by('-vote_date')[0]
            if choice == 'like':
                pData.num_likes -= 1
                newVal = pData.num_likes
                
            elif choice == 'dislike':
                pData.num_dislikes -= 1
                newVal = pData.num_dislikes
                
            xml = '<xml><data><iddata>'+str(int(newVal))+'</iddata><valdata>'+str(prjid)+'</valdata></data></xml>'
            pData.save()
            oldLike.delete()
        else:
            xml = '<xml><error>Invalid choice "' + choice + '" selected</error></xml>'
        return HttpResponse(xml, content_type="text/xml")

def like(request, projectid):
    ''' Liking and disliking. '''
    
    #Databases clicks of the like and dislike buttons
    # Has the form been submitted?

    if request.method == 'GET': 
        
        # Parse the projectid
        splt = projectid.split('_')
        
        prjid = splt[1]
        choice = splt[0]
 
        if choice in ['like', 'dislike']:
 
            #Now record this in the db
            pData = projectModel.objects.filter(id=prjid)[0]
            newLike = projectVoteModel(project=pData, vote_date=datetime.now(), vote_type = choice)

            if choice == 'like':
                pData.num_likes += 1
                newVal = pData.num_likes
	            
            elif choice == 'dislike':
                pData.num_dislikes += 1
                newVal = pData.num_dislikes
                
            xml = '<xml><data><iddata>'+str(int(newVal))+'</iddata><valdata>'+str(prjid)+'</valdata></data></xml>'            
            pData.save()
            newLike.save()
        else:
            xml = '<xml><error>Invalid choice "' + choice + '" selected</error></xml>'
        return HttpResponse(xml, content_type="text/xml")
    
def project_gallery(request):

    ''' Display all the projects as table list of icons'''
    c = {"classification":"unclassified","page_title":"iStarter Project Gallery"}
    c.update(csrf(request))
    pData = projectModel.objects.values_list('title','pub_date','description', 'num_backers', 'pk', 'importance', 'effort', 'resource', 'active', 'num_likes', 'num_dislikes')
    rowdict = {'title':'','pub_date':'','description':'','backPercentage':'','backersRequired':'','id':'', 'importance':'', 'effort':'', 'resource':'', 'active':'','num_likes':'','num_dislikes':''}

    #Template for model outputs
    template_headings = [{'db':'title', 'pretty':'Idea Title'}, 
                         {'db':'pub_date', 'pretty':'Date Published'},
                        {'db':'description', 'pretty':'Idea Description'},
                        {'db':'num_backers', 'pretty':'Number of Backers'},
                        {'db':'pk','pretty':'Project Id'},
						{'db':'importance','pretty':'Importance of task'},
                        {'db':'effort','pretty':'Level of Effort required'},
                        {'db':'resource','pretty':'Resources required'},
                        {'db':'active','pretty':'Project is Active'},
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

	# Prepare the data to pass to the HTML
	outrow = []
	out = []
	
	for pDataidx, row in enumerate(pData):
		for headingidx, heading in enumerate(template_headings):
			if heading['db']=='num_backers' :
				num_backers = row[headingidx]
			if heading['db']=='importance' :
				imp=row[headingidx]
			if heading['db']=='effort' :
				eff=row[headingidx]	
			if heading['db']=='resource' :
				res=row[headingidx]	
		
		backersRequired = backersRequiredAlgorithm(eff, imp, res)		
		#backersRequired = eff * ((6-imp)**2) * (res**3)
		backPercentage  = 100 * num_backers / backersRequired	
		rowdict['backPercentage'] = int(backPercentage)
		rowdict['backersRequired'] = backersRequired
		
		for headingidx, heading in enumerate(template_headings):
			if heading['db']=='title' :
				rowdict['title'] = row[headingidx][:20]
			if heading['db']=='pub_date' :
				rowdict['pub_date'] = row[headingidx]
			if heading['db']=='description' :
				rowdict['description'] = row[headingidx][:200]
			if heading['db']=='num_backers' :
				rowdict['num_backers'] = row[headingidx]
			if heading['db']=='pk':
				rowdict['id']=row[headingidx]
			if heading['db']=='importance':
				rowdict['importance'] = row[headingidx]
			if heading['db']=='effort':
				rowdict['effort'] = row[headingidx]
			if heading['db']=='resource':
					rowdict['resource'] = row[headingidx]
			if heading['db']=='active' :
				# assign a couple of projects a sbeing active to test its all working
				if pDataidx == 2 or pDataidx==4 :
					rowdict['active']= 1 # row[headingidx]
				else:
					rowdict['active']= 0 # row[headingidx]
			if heading['db']=='num_likes' :
				rowdict['num_likes']=int(row[headingidx])
			if heading['db']=='num_dislikes' :
				rowdict['num_dislikes']=int(row[headingidx])				
        	outrow.append(rowdict.copy())
		out.append(outrow)
		outrow = []
	c['tableData'] = out
	#c['headings'] = template_headings
	
	return render_to_response("projectsapp/project_gallery.html", c)

#----------------------------------------------------------------------------------------

def project_gallery_filtered(request):
    ''' Display some of the projects, depending on filter parameters'''
    
    #TODO: Update this classification dynamically based on highest value in data
    c = {"page_title":"iSTARter Project Gallery"}
    
    # Get the headings data
    c['headings'] = settings.TEMPLATE_HEADINGS
    
    # Get the request parameters from the url - into a dictionary
    params = request.GET.dict()
    safeParams = validateQueryParams(params)

    # Get the data, having handled the sorting and filtering 
    resultSet = filteredRetrieval(projectModel, safeParams)

    # Get the project max classification
    c['classification'] = getMaxClassification(resultSet) or 'unknown'
    
    # Create the tag list for selecting by user
    c['known_tags'] = distinctTagsSortedAlpha()

    # Get the urls needed to filter the results when someone clicks on them
    c['sorts_and_filters'] = buildSingleSortAndFilterItems()
    
    # Get the fields we want out into a list
    flds = [f['db'] for f in settings.TEMPLATE_HEADINGS]
    
    # Now get a list containing each row stored as a dict
    data = resultSet.values(*flds)
    
    allRows = []
    rowList = []
    i = 0
    for row in data:
        row['id'] = row['pk']
        backersRequired = brAlg(row[settings.EFFORT_FIELD], row[settings.IMPORTANCE_FIELD], row[settings.RESOURCE_FIELD])        
        backPercentage  = 100 * row[settings.NUM_BACKERS] / backersRequired    
        row['backPercentage'] = int(backPercentage)
        row['backersRequired'] = backersRequired
        rowList.append(row)
    
    # Now whack it into another list for good measure - never have enough ;)
    c['tableData'] = rowList
    
    return render_to_response("projectsapp/project_gallery.html", c)    

#----------------------------------------------------------------------------------------

def project_detail(request,projid):
    ''' Display detail on a project '''

    outData = projectModel.objects.get(pk=int(projid))
    rowdict = {'title':'','pub_date':'','description':'','num_backers':'','id':'','backPercentage':'',
               'importance':'','effort':'','resource':'', 'active':'','backersRequired':'','effort_list':[],
                'importance_list':[],'resource_list':[], 'num_likes':0,'num_dislikes':0}
    
    #Template for model outputs
    template_headings = [{'db':'title', 'pretty':'Idea Title'}, 
                         {'db':'pub_date', 'pretty':'Date Published'},
                        {'db':'description', 'pretty':'Idea Description'},
                        {'db':'num_backers', 'pretty':'Number of Backers'},
                        {'db':'importance','pretty':'Importance'},
                        {'db':'effort','pretty':'Effort'},
                        {'db':'resource','pretty':'Resource'}]

    #Prepare the data to pass to the HTML
    #rowdict['title'] = outData.title
    rowdict['pub_date'] = outData.pub_date
    rowdict['description'] = outData.description
    rowdict['num_backers'] = outData.num_backers
    rowdict['num_likes'] = int(outData.num_likes)
    rowdict['num_dislikes'] = int(outData.num_dislikes)

    rowdict['importance'] = outData.importance
    rowdict['effort'] = outData.effort
    rowdict['effort_list'] = range(outData.effort)
    rowdict['importance_list'] = range(outData.importance)
    rowdict['resource_list'] = range(outData.resource)
    rowdict['resource'] = outData.resource

    rowdict['id']=projid
    backersRequired = rowdict['effort'] * ((6-rowdict['importance'])**2) * (rowdict['resource']**3)
    rowdict['backersRequired']=backersRequired
    rowdict['backPercentage'] = 100 * rowdict['num_backers'] / backersRequired
    rowdict['active'] = outData.active
    c = {"classification":"unclassified","page_title":outData.title}
    c.update(csrf(request))
    c['data'] = rowdict
    c['headings'] = template_headings    
    
    
    '''Ideas gallery - yes should import this but times tight... '''
    pideaData = outData.ideas_derived_from.values_list('title','pub_date','description', 'pk', 'likes', 'dislikes', 'id')
    #print pideaData
    max_likes = ideaModel.objects.all().aggregate(Max('likes'))
    max_dislikes = ideaModel.objects.all().aggregate(Max('dislikes'))
    outdict = {'title':'','pub_date':'','description':'','likes':0,'dislikes':0, 'perc_likes':0,'perc_dislikes':0, 'linked_projects':[]}
    out = []
    #Simpler
    for row in pideaData:
        outdict['title']=row[0][:15]
        outdict['pub_date']=row[1]
        outdict['description']=row[2][:100]
        outdict['likes']=int(row[4])
        outdict['dislikes']=int(row[5])
        outdict['perc_likes']=100*outdict['likes']/max_likes['likes__max']
        outdict['perc_dislikes']=100*outdict['dislikes']/max_dislikes['dislikes__max']
        outdict['id'] = row[3]
        projs = projectModel.objects.filter(ideas_derived_from=row[3])
        if projs:
            for proj in projs:
                outdict['linked_projects'].append(proj.id)
        out.append(outdict.copy())
        #print outdict
        outdict['linked_projects']=[]
      

    c['tableData_ideas'] = out
    
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
                
                return render_to_response('projectsapp/back_thanks.html', c)
                
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

def learn_more(request) :
	c = {"classification":"unclassified",
         "page_title":"Learn More:"}
	c.update(csrf(request))
	return render_to_response('projectsapp/Learn_more.html', c)
    
