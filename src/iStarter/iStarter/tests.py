"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
#from ideasapp.models import idea as ideaModel
from datetime import datetime, timedelta
from random import randint, choice
import importlib
import inspect
import sys
import os
import json
#Uncmment this when deplpoyed with django
#import ideasapp.settings as dataloadsettings

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)


class testData():
    def __init__(self, testDataPath, nounsfile, headersfile,
                 classifications,fixtureOutPath,fixtureDateFname):   
    #Paths for where the input test data is stored
        print 'Loading test data'
        fh = open(testDataPath+'/'+nounsfile,'r')
        self.words = []
        while fh.readline():
            self.words.append(fh.readline().rstrip('\r\n'))
        fh.close()
        print 'Got test words'
        
        fh = open(testDataPath+'/'+headersfile,'r')
        self.headers = fh.read()
        fh.close()
        print 'Got test headers'
        
        self.classifications = classifications
        print 'got classification'
        
        self.fixtureOutPath = fixtureOutPath
        print 'Got fixture out path'
        
        self.fixtureDateFname = fixtureDateFname
        print 'Got fixture data fname'
        
    
    def randomDate(self):
        #Makes Random date
        dtg = datetime.now() - timedelta(days = randint(0,365*5), seconds = randint(0, 86399), microseconds = randint(0, 999999))
        return dtg.isoformat()
    
    def randomText(self,chars):
        #Makes random text - chars is the number of characters allow max
        #Can be used for titles or body text etc
        #Make the title from words - randomise the amoutn we return up to max words
        title = ''
        while len(title) < randint(1,chars):
            title = title+' '+choice(self.words)
        #Clean it up a little
        title.strip()
        title=title[:chars]
        return title
        
    def randomEmail(self):
        #Makes random email address
        names = ['rich','bob','dave','ted','pete','phil','wendy','giles','mortimer']
        email = choice(names)+'@'+choice(self.words)+'.com'
        return str(email)
   
    def randomTags(self):
        ''' Adds a randomly selected bunch of tags to the object'''

   

    ## MRN - I've had to put some model specific bits of code in here, which has made me
    ##       quite, quite sad. I think the best way around this would be for each app to
    ##       define a class which inherits this class, and just tweeks the following
    ##       function appropriately. I don't think this would be hard to do, but its a
    ##       low priority at the moment - but might have paybacks over the years as it
    ##       will be able to be reused in all future django apps.
    def buildInitalData(self, appname, rows):
        #Gets all info on fields within all models under supplied appname
        #Then builds the initial_data.json file from JSON created here
        #WARNING - doesnt yet check if the class within 'model.py' is of model type 
        #Input is django application name as string and number of rows to add
        #TODO: Try/excepts
        #TODO: more data types
        #Get all models in the app model module
        print '*'*50
        i = importlib.import_module(appname+'.models')
        #find all classes - i.e. models
        #TODO: Put extra check here to make sure its a model... and not some other class in the model module
        clsmembers = inspect.getmembers(sys.modules[appname+'.models'], inspect.isclass)
        
        jsonout = []
        #Iterate over models
        for cls in clsmembers:
            if cls[0] != 'ideaModel' or appname != 'projectsapp':
                print cls
                i = importlib.import_module(appname+'.models', cls[0])
                model = getattr(i, cls[0]) 
                #RB: Catch to ignore for model managers
                try:
                    fields = model._meta.fields
                except:
                    continue

                fields = model._meta.fields
                jsonfields = {}
                for field in fields:
                    #print field, field.get_internal_type()
                    #Make blank json dict
                    if field.get_internal_type() != 'AutoField':
                        jsonfields[field.name]=''
                for i in xrange(rows):
                    #Iterate for number of rows we want loaded in
                    #Iterate over fields 
                    for field in fields:
                        if field.get_internal_type() == 'CharField' and field.name.find('classification') != -1:
                            jsonfields[field.name]=choice(self.classifications)[0]
                        elif field.get_internal_type() == 'CharField' and field.name.find('header') != -1:                  
                            jsonfields[field.name]=self.headers
                        elif field.get_internal_type() == 'ForeignKey':
                            jsonfields[field.name] = randint(0,rows-1)
                        #All other Char fields2.
                        #TODO: Add more options for different char field types
                        elif field.get_internal_type() == 'CharField':
                            jsonfields[field.name]=self.randomText(field.max_length)                        
                        elif field.get_internal_type() == 'IntegerField':                   
                            jsonfields[field.name]=randint(0,5000)
                        elif field.get_internal_type() == 'DateTimeField':                    
                            jsonfields[field.name]=self.randomDate()
                        elif field.get_internal_type() == 'EmailField':
                            jsonfields[field.name]=self.randomEmail()
                        elif field.get_internal_type() == 'BooleanField':
                            jsonfields[field.name]='True'
                        elif field.get_internal_type() == 'FloatField':
                            jsonfields[field.name]=1
                        else:
                            continue
                    if cls[0] == 'project' and appname == 'projectsapp':
                        jsonfields['ideas_derived_from'] = []
                        for ids in xrange(randint(1,10)):
                            jsonfields['ideas_derived_from'].append(randint(0,rows-1))                      

                    #copy the dict
                    #jsonfields_ = jsonfields.copy()
                    jsonout.append({'model':appname+'.'+cls[0], 'pk':i, 'fields':jsonfields.copy()})
                
            #print jsonout
        self.saveJson(jsonout, appname)
        return   
        
    def saveJson(self, jsonout, appname):
       #Dump json out to a file for initial data to import on syncdb
       if not os.path.exists(self.fixtureOutPath+'/'+appname+'/fixtures'):
           os.mkdir(self.fixtureOutPath+'/'+appname+'/'+'fixtures')

       with open(self.fixtureOutPath+'/'+appname+'/'+'fixtures/'+self.fixtureDateFname, 'w') as outfile:
           json.dump(jsonout, outfile)
           outfile.close()
       return


def addTagsPerRow(testDataPath, appName):
    ''' Adds a series of tags per row '''
    
    
    f = open(os.path.join(testDataPath, 'nouns.txt'), 'r')
    words = [line.replace('\r\n', '') for line in f.readlines()]
    f.close()
    
    # Get the correct model to work with
    importlib.import_module(appName+'.models')
    clsMembers = inspect.getmembers(sys.modules[appName+'.models'], inspect.isclass)
    
    for cls in clsMembers:
        
        i = importlib.import_module(appName+'.models', cls[0])
        model = getattr(i, cls[0])

        #RB: Catch to ignore for model managers
        try:    fields = model._meta.fields
        except: continue

        # Get all of the rows
        targetRows = model.objects.all()
        
        # Check that the object has a field called tags. If not, move on.
        try:
            tags = targetRows[0].tags.all()
        except:
            continue
        
        print "%s:\t Adding random tag data for each row/object." %appName,
        
        # For each row, chuck in between 20 and 50 random tags.
        for r in range(20):
            for i in range(randint(1, 5)):
                targetRows[r].tags.add(choice(words[0:50]))
            targetRows[r].tags.add('xxx_test_tag')
            targetRows[r].save()
            
        # Make sure they're definitely in there.
        res = model.objects.filter(tags__name__in=["xxx_test_tag"])
        if len(res) > 0:
            print ": success."
        else:
            print ": fail."


    
