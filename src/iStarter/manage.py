#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "iStarter.settings")

    from django.core.management import execute_from_command_line
    from iStarter.settings import config_module
    #If its a syncdb then first we create some JSON and save it to the initial_data.json
    #in the fixtures folder under each app
    #...so it loads this data in as part of the syncdb
    if sys.argv == ['manage.py','syncdb'] and config_module.testDataChk==True:
        
        from iStarter.tests import testData
        from ideasapp.settings import CLASSIFICATIONS        
        #Make the fixutres data file based on models in our appslist
        try:
            r = testData(config_module.testDataPath, config_module.nounsfile, 
                         config_module.headersfile, CLASSIFICATIONS, 
                         config_module.fixtureOutPath, config_module.fixtureDateFname)
        except:
            print 'Failed to initialise all test data - check paths in your config', sys.exc_info()[0]
            sys.exit()
        for app in config_module.testDataAppsList:
            try:
                out = r.buildInitalData(app, config_module.testDataNumRows)
                print 'Wrote inital_data.json for {0}'.format(app)
            except Exception, e:
                print 'Failed to write initial_data.json for {0}'.format(app), e
        #Now fire the command line 
        execute_from_command_line(sys.argv)
    else:
        #Just fire the command line 
        execute_from_command_line(sys.argv)
