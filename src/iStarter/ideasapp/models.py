from django.db import models

# Create your models here.

class idea(models.Model):
    def __unicode__(self):
        return self.title
    idea_title = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date_published')
    idea_text = models.CharField(max_length=2000)
    idea_id = models.CharField(max_length=100)
    num_backers = models.IntegerField()
    names_backers = models.CharField(max_length=20000)
    name_starter = models.CharField(max_length=100)
    email_starter = models.CharField(max_length=100)
    verified = models.BooleanField()
    date_verified = models.DateTimeField('date_verified')
    verified_by = models.CharField(max_length=100)
    
    # A couple of others
    idea_classification = models.CharField(max_length=100)
    idea_headers = models.CharField(max_length=20000)