from django.shortcuts import render_to_response
from django.core.context_processors import csrf

import os
import sys
import logging
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


def submit(request):
    ''' Pulling together ideas into a glorious project. '''

    c = {"classification":"unclassified",
         "page_title":"My Glorious Project"}
    c.update(csrf(request))
    print c
    return render_to_response('projectsapp/project_submit.html', c)
