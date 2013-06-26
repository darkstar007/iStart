#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "iStarter.settings")

    from django.core.management import execute_from_command_line
    '''
    #If its a syncdb then first we create some JSON and save it to the initial_data.xml
    #...so it loads this data in as part of the sync
    from config.dev_cn import testDataLoad, testDataAppsList, testDataNumRows, testDataPath, nounsfile, headersfile
    from ideasapp.tests import testData  
    from ideasapp.settings import CLASSIFICATIONS
    if sys.argv == ['manage.py','syncdb'] and testDataLoad == True:
        #Load test data - based on list of models in config
        #Instantiate testdata loader
        r = testData(testDataPath, nounsfile, headersfile, CLASSIFICATIONS)
        for app in testDataAppsList:
            out = r.loadDataToModels(app, testDataNumRows)
            print out        
    '''
    #Now fire the command line syncdb
    execute_from_command_line(sys.argv)