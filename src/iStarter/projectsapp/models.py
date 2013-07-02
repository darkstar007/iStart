from django.db import models

import sys
sys.path.append('..')
from ideasapp.models import idea as ideaModel

# Create your models here.

class project(models.Model):
    title = models.CharField(max_length=200, unique = True)  # The title
    pub_date = models.DateTimeField('date_published')
    description = models.CharField(max_length=2000) # The main text
    #idea_id = models.CharField(max_length=100)
    '''Ommitted these to make life easier at the start...'''

    #name_starter = models.CharField(max_length=100)
    #email_starter = models.CharField(max_length=100)
    verified = models.BooleanField()
    #date_verified = models.DateTimeField('date_verified')
    #verified_by = models.CharField(max_length=100)
    # A couple of others
    classification = models.CharField(max_length=100) 
    headers = models.CharField(max_length=20000)

    ideas_derived_from = models.ManyToManyField(ideaModel, related_name='title+')

    #def __unicode__(self):
        #return self.idea_title
    

class pvote(models.Model):
    project = models.ForeignKey(project)
    vote_date = models.DateTimeField('voted_on_date')
    username = models.CharField(max_length=128)
    weight = models.IntegerField()
