import datetime
import copy
import projectsapp.settings as settings
from projectsapp.models import project as projectModel
from django.test import TestCase
from projectsapp.code import getMaxClassification

class TestGetClassification(TestCase):

    def setUp(self):
        
        self.classifications = list(settings.CLASSIFICATIONS)
        
        # Instantiate object
        self.proj = projectModel(
                             title="an excellent project",
                             pub_date=datetime.datetime.utcnow(),
                             description="here's a great project",
                             num_backers=1,
                             num_likes=1,
                             num_dislikes=0,
                             classification="unclassified",
                             headers="headers here;and here",
                             verified=True,
                             importance=1,
                             effort=1,
                             resource=1,
                             active=1
                             )

        # Create a row for each different classification string in it
        for i in range(len(self.classifications)):
            newProj = copy.deepcopy(self.proj)
            newProj.title += ' '+str(i)
            newProj.classification = self.classifications[i][0].lower()
            newProj.save()

    def tearDown(self):
        ''' Remove content from the db'''
        projectModel.objects.all().delete()

    def testGetMaxClassificationRestricted(self):
        '''Tests for a normal case of a range of classifications'''
        
        results = projectModel.objects.all().filter(classification='restricted')
        maxClass = getMaxClassification(results)
        self.assertEquals(maxClass, 'restricted')

    def testGetMaxClassificationNormal(self):
        '''Tests for a normal case of a range of classifications'''
        
        results = projectModel.objects.all()
        maxClass = getMaxClassification(results)
        self.assertEquals(maxClass, self.classifications[-1][0].lower())
        
    def testGetMaxClassificationNoResults(self):
        ''' Test for the case where there are no results - default to ts'''
        results = projectModel.objects.all().filter(title='job')
        maxClass = getMaxClassification(results)
        self.assertEquals(maxClass, self.classifications[0][0].lower())


    def testGetMaxClassificationUnknown(self):
        ''' Tests for the case where there is an unknown classification in it'''
        
        # Make a new one
        newProj = copy.deepcopy(self.proj)
        newProj.title = 'yahooo'
        newProj.classification = 'banana'
        newProj.save()
        
        # Get them all back
        results = projectModel.objects.all()
        
        maxClass = getMaxClassification(results)
        self.assertEquals(maxClass, self.classifications[-1][0].lower())
        