from django.db import models

# Create your models here.

class project(models.Model):
    project_title = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date_published')