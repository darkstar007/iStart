from django.db import models

# Create your models here.

import sys
sys.path.append('..')
from ideasapp.models import idea

class project(idea):
    ideas_derived_from = models.CharField(max_length=4096)
