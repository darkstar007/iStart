"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
#from ideasapp.models import idea as ideaModel
from datetime import datetime
from random import randint
import importlib
import inspect
import sys
#Uncmment this when deplpoyed with django
#import ideasapp.settings as dataloadsettings

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)


class testData():
    def __init__(self, testDataPath, nounsfile, headersfile, classifications):   
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
    
    def randomDate(self):
        #Makes Random date
        dtg = datetime(randint(2012,2015),randint(1,12),randint(1,28),randint(0,23),randint(0,59),randint(0,59))
        return dtg
    
    def randomText(self,chars):
        #Makes random text - chars is the number of characters allow max
        #Can be used for titles or body text etc
        #Make the title from words
        title = ''
        while len(title) < chars:
            title = title+' '+self.words[randint(0,len(self.words))]
        #Clean it up a little
        title.strip()
        title=title[:chars]
        return title
        
    def randomEmail(self):
        #Makes random email address
        names = ['rich','bob','dave','ted','pete','phil','wendy','giles','mortimer']
        email = names[randint(0,len(names))]+'@'+self.words[randint(0,len(self.words))]+'.com'
        return str(email)
   
    def buildInitalData(self, appname, rows):
        #Not working yet
        #TODO: Just need to build JSON output from each of the conditions below
        #Gets all info on fields within all models under supplied appname
        #Then builds the initial_data.xml file from JSON created here
        #WARNING - doesnt yet check if the class within 'model.py' is of model type 
        #Input is django application name as string
        #TODO: Try/excepts
        #TODO: more data types
        #TODO: flags to select which models you want data to be loaded into
        #Get all models in the app model module
        i = importlib.import_module(appname+'.models')
        #find all classes - i.e. models
        fixtureData = []
        #TODO: Put extra check here to make sure its a model... and not some other class in the model module
        clsmembers = inspect.getmembers(sys.modules[appname+'.models'], inspect.isclass)
        #Iterate over models
        for cls in clsmembers:
            i = importlib.import_module(appname+'.models', cls[0])
            model = getattr(i, cls[0]) 
            fields = model._meta.fields
            #Iterate over fields 
            if field.get_internal_type() == 'CharField' and field.name.find('classification') != -1:
                
            elif field.get_internal_type() == 'CharField' and field.name.find('header') != -1:                  
                
            #All other Char fields
            #TODO: Add more options for different char field types
            elif field.get_internal_type() == 'CharField':
                text = self.randomText(field.max_length)                        
                
            elif field.get_internal_type() == 'IntegerField':                   
                
            elif field.get_internal_type() == 'DateTimeField':                    
                out = model(name=self.randomDate())
                out.save()
            elif field.get_internal_type() == 'EmailField':
                out = model(name=self.randomEmail())
                out.save()
            else:
                continue
            fieldInfo.append({'model':appname+'.'+cls[0],'fields':field.name})            
        return 'Added {0} rows to all models under app: {1}'.format(rows, appname)   
   
   
'''        
    def loadDataToModels(self, appname, rows):
        #Not working!!
        #Gets all info on fields within all models under supplied appname
        #Reads data into database using above random funcs
        #WARNING - doesnt yet check if the class within 'model.py' is of model type 
        #Input is django application name as string
        #TODO: Try/excepts
        #TODO: too many saves
        #TODO: more data types
        #TODO: flags to select which models you want data to be loaded into
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
            #Iterate over fields adding data p to rows flag
            for i in range(0,rows,1):
                for field in fields:
                    name = field.name
                    print name
                    #Loop through - get data type, max length etc, import and necessary
                    #Classification field checker - not that robust!
                    if field.get_internal_type() == 'CharField' and field.name.find('classification') != -1:
                        out = model(name__exact=self.classifications[0][randint(len(self.classifications))])
                        out.save()
                    elif field.get_internal_type() == 'CharField' and field.name.find('header') != -1:                  
                        out = model(name=self.headers)
                        out.save()
                    #All other Char fields
                    #TODO: Add more options for different char field types
                    elif field.get_internal_type() == 'CharField':
                        text = self.randomText(field.max_length)                        
                        out = model(name__exact=text)
                        out.save()
                    elif field.get_internal_type() == 'IntegerField':                   
                        out = model(name=self.randint(0,5000))
                        out.save()
                    elif field.get_internal_type() == 'DateTimeField':                    
                        out = model(name=self.randomDate())
                        out.save()
                    elif field.get_internal_type() == 'EmailField':
                        out = model(name=self.randomEmail())
                        out.save()
                    else:
                        continue
                #fieldInfo.append({'modelname':cls[0],'fieldname':field.name,'fieldtype':field.get_internal_type(),'field_max_len':field.max_length})            
        return 'Added {0} rows to all models under app: {1}'.format(rows, appname)
'''
        
        
        