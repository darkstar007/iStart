from django.db import models

from taggit.managers import TaggableManager

# Create your models here.

class idea(models.Model):
    
    title = models.CharField(max_length=200, unique = True)  # The title

    pub_date = models.DateTimeField('date_published')
    description = models.CharField(max_length=2000) # The main text
    #idea_id = models.CharField(max_length=100)
    num_backers = models.IntegerField()
    '''Ommitted these to make life easier at the start...'''
    #names_backers = models.CharField(max_length=20000)
    #name_starter = models.CharField(max_length=100)
    #email_starter = models.CharField(max_length=100)
    verified = models.BooleanField()
    #date_verified = models.DateTimeField('date_verified')
    #verified_by = models.CharField(max_length=100)
    # A couple of others
    classification = models.CharField(max_length=100) 
    headers = models.CharField(max_length=20000)

    #def __unicode__(self):
        #return self.idea_title

    # This stores the tags provided in the text input box and those
    # that a user has clicked from the pre-existing list.
    tags = TaggableManager()
    
