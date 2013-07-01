"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
#from ideasapp.models import idea as ideaModel
from datetime import datetime
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
        fh = open(testDataPath+'/'+headersfile,'r')
        self.headers = fh.read()
        fh.close()
        self.classifications = classifications
        self.fixtureOutPath = fixtureOutPath
        self.fixtureDateFname = fixtureDateFname
    
    def randomDate(self):
        #Makes Random date
        dtg = datetime(randint(2012,2015),randint(1,12),randint(1,28),randint(0,23),randint(0,59),randint(0,59))
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
   
    def buildInitalData(self, appname, rows):
        #Gets all info on fields within all models under supplied appname
        #Then builds the initial_data.json file from JSON created here
        #WARNING - doesnt yet check if the class within 'model.py' is of model type 
        #Input is django application name as string and number of rows to add
        #TODO: Try/excepts
        #TODO: more data types
        #Get all models in the app model module
        i = importlib.import_module(appname+'.models')
        #find all classes - i.e. models
        #TODO: Put extra check here to make sure its a model... and not some other class in the model module
        clsmembers = inspect.getmembers(sys.modules[appname+'.models'], inspect.isclass)
        #Iterate over models
        for cls in clsmembers:
            i = importlib.import_module(appname+'.models', cls[0])
            model = getattr(i, cls[0]) 
            fields = model._meta.fields
            jsonfields = {}
            for field in fields:
                #print field, field.get_internal_type()
                #Make blank json dict
                if field.get_internal_type() != 'AutoField':
                    jsonfields[field.name]=''
            jsonout = []
            for i in range(0,rows):
                #Iterate for number of rows we want loaded in
                #Iterate over fields 
                for field in fields:
                    if field.get_internal_type() == 'CharField' and field.name.find('classification') != -1:
                        jsonfields[field.name]=choice(self.classifications)[0]
                    elif field.get_internal_type() == 'CharField' and field.name.find('header') != -1:                  
                        jsonfields[field.name]=self.headers
                    #elif field.get_internal_type() == 'OneToOneField':
                    #    jsonfields[field.name] = randint(0,rows-1)
                    #All other Char fields
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
                    else:
                        continue
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

