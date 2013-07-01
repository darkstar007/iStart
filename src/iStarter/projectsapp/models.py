from django.db import models

# Create your models here.

import sys
sys.path.append('..')
from ideasapp.models import idea as ideaModel

class project(ideaModel):
    
    ideas_derived_from = models.ManyToManyField(ideaModel, related_name='title+')

