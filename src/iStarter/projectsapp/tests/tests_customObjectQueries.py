import os
import copy
import random
import datetime
import time
import projectsapp.settings as settings
from projectsapp.customObjectQueries import filteredRetrieval, validateQueryParams, tagBasedFilter, exactMatchFilter, sortedResults
from projectsapp.models import project as projectModel

from django.test import TestCase

class TestsValidateQueryParams(TestCase):
      
    def testNoParameters(self):
        """
        Checks for instance where there are no url params
        """
        params = {}
        safeParams = validateQueryParams(params)
        self.assertEquals(safeParams, {})

    def testErroneousParameter(self):
        """
        Checks for instance where there is a parameter not in any of the valid lists
        """
        params = {'duck':'quack'}
        safeParams = validateQueryParams(params)
        self.assertEquals(safeParams, {})

    def testErroneousParameterValue(self):
        """
        Checks for instance where parameter is valid, but its value isn't
        """
        
        validFld = random.choice(settings.VALID_FILTERS.keys())
        params = {validFld : 'quack'}
        safeParams = validateQueryParams(params)
        self.assertEquals(safeParams, {})
        
    def testValidFilterParams(self):
        """
        Check that the parameter key is acceptable
        """
        validFld = random.choice(settings.VALID_FILTERS.keys())
        acceptableValue = random.choice(settings.VALID_FILTERS[validFld])
        params = {validFld : acceptableValue}
        safeParams = validateQueryParams(params)
        self.assertEquals(safeParams, {validFld:acceptableValue})

    def testBothValidAndInvalidParams(self):
        """
        Check for 1 good parameter and 1 bad parameter
        """
        validFld = random.choice(settings.VALID_FILTERS.keys())
        acceptableValue = random.choice(settings.VALID_FILTERS[validFld])
        params = {validFld : acceptableValue}
        params['duck'] = 'quack'
        validFld2 = random.choice(settings.VALID_FILTERS.keys())
        while params.has_key(validFld2) == False:
            params[validFld2] = 'quack2'
            break
        safeParams = validateQueryParams(params)
        self.assertEquals(safeParams, {validFld:acceptableValue})
        
#========================================================================================

class TestsCustomFilters(TestCase):
    ''' Should work out the full range of possibilities here
    
    '''

    def setUp(self):
        
        words = ['homer', 'bart', 'marge', 'moe', 'lisa', 'apu', 'maggie', 'santos']
        
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
        for i in range(5):
            newProj = copy.deepcopy(self.proj)
            newProj.title += ' '+str(i)
            newProj.importance += i
            newProj.num_backers += 100000 + i
            newProj.pub_date=datetime.datetime.utcnow()
            newProj.save()

            newProj.tags.add(words[i])
            newProj.save()
            
        self.results = projectModel.objects.all()
            
    def tearDown(self):
        ''' Remove content from the db'''
        projectModel.objects.all().delete()


    def testTagBasedFilterSingleTagGotResult(self):
        ''' Tests being able to filter down a result set based on the tags '''

        params = {'tags':'homer'}
        results = tagBasedFilter(self.results, params)
        self.assertEqual(len(results), 1)

    def testTagBasedFilterSingleTagNoResult(self):
        ''' Tests being able to filter down a result set based on the tags '''

        params = {'tags':'larry'}
        results = tagBasedFilter(self.results, params)
        self.assertEquals(bool(results), False)

    def testTagBasedFilterMultipleTags(self):
        ''' Tests being able to filter down a result set based on the tags '''
 
        params = {'tags':'homer,marge'}
        results = tagBasedFilter(self.results, params)
        self.assertEquals(len(results), 2)
 

    def testExactMatchFilter(self):
        ''' Tests being able to filter down based on exact filter '''

        params = {'importance':'1'}
        
        results = exactMatchFilter(self.results, params)
        self.assertEquals(len(results), 1)
 
    def testExactMatchFilterMulti(self):
        
        params = {'importance':'1',
                  'active' : '0'}
        newProj = copy.deepcopy(self.proj)
        newProj.active=0
        newProj.save()
        
        results = exactMatchFilter(self.results, params)
        self.assertEquals(len(results), 1)
        
    def testSortedResultsSingleAscending(self):
        ''' Tests being able to filter down based on exact filter '''

        params = {'sort':'importance;1'}
        
        results = sortedResults(self.results, params)
        importanceOrder = []
        for res in results:
            importanceOrder.append(res.importance)
        
        self.assertEquals(importanceOrder[0:5], [1, 2, 3, 4, 5])
        
    def testSortedResultsSingleDescending(self):
        ''' Tests being able to filter down based on exact filter '''

        params = {'sort':'num_backers;-1'}
        
        results = sortedResults(self.results, params)
        order = []
        for res in results:
            order.append(res.num_backers)

        self.assertEquals(order[:5], [100005, 100004, 100003, 100002, 100001])

    def testSortedResultsPubDate(self):
        ''' Tests being able to filter down based on exact filter '''

        params = {'sort':'pub_date;-1'}
        
        results = sortedResults(self.results, params)
        order = [res.pub_date for res in list(results)][:5]
        # Get the time now as a starting point to difference backwards
        newer = datetime.datetime.utcnow()
        for ts in order:
            self.assertTrue(newer > ts)
            ts = newer
        
        
    def testSortedResultsMulti(self):
        ''' Tests being able to filter down based on exact filter '''

        params = {'sort':'num_backers;-1,importance;1'}
        
        results = sortedResults(self.results, params)
        order = []
        for res in results:
            order.append(res.title)
            #print res.title
        
        ##TODO: Finish this test
        #TODO: Work out why there is still data in the db despite it getting deleted.

    def testfilteredRetrieval_tagFilteredOnly(self):
        ''' Tests being able to retrieve the right combination of results '''



    def testfilteredRetrieval_exactFilteredOnly(self):
        ''' Tests being able to retrieve the right combination of results '''

    def testfilteredRetrieval_sortOnly(self):
        ''' Tests being able to retrieve the right combination of results '''

#========================================================================================

class TestsFilteredRetrieval(TestCase):
    ''' 
    Tie together sorting, tag filtering and discrete filtering
    '''

    def setUp(self):
        ''' Build me some data'''
        
        words = ['homer', 'bart', 'marge', 'moe', 'lisa', 'apu', 'maggie', 'santos']
        
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
        for i in range(5):
            newProj = copy.deepcopy(self.proj)
            newProj.title += ' '+str(i)
            newProj.importance += i
            newProj.num_backers += 100000 + i
            newProj.pub_date=datetime.datetime.utcnow()
            newProj.save()
            newProj.tags.add(words[i])
            newProj.save()

        self.results = projectModel.objects.all()
            
    def tearDown(self):
        ''' Remove content from the db'''
        
        projectModel.objects.all().delete()

    def testAllResultsNoFilterNoSort(self):
        ''' Tests against straight retrieval of everything'''

        params = {}
        results = filteredRetrieval(projectModel, params)
        self.assertEquals(len(results), 5)

    # ------------------------------------------------------------
    # BASIC
    def testJustTags(self):
        ''' Tests against just tags in the params dict'''

        params = {'tags':'homer'}
        results = filteredRetrieval(projectModel, params)
        self.assertEquals(len(results), 1)
        

    def testJustFieldFilter(self):
        ''' Tests against just field-based filtering'''
        
        params = {'importance':'1'}
        results = filteredRetrieval(projectModel, params)
        self.assertEquals(len(results), 1)
        
    
    def testJustSort(self):
        ''' Tests against just sorted results'''
    
        params = {'sort':'pub_date;-1'}
        results = filteredRetrieval(projectModel, params)
        self.assertEquals(len(results), 5)
        order = [res.pub_date for res in list(results)][:5]

        # Get the time now as a starting point to difference backwards
        newer = datetime.datetime.utcnow()
        for ts in order:
            self.assertTrue(newer > ts)
            ts = newer

    # ------------------------------------------------------------
    # STITCHED 2 TOGETHER
      
    def testTagsAndSort(self):
        ''' Tests against tag filter and a sort'''

        params = {'tags':'homer,marge,bart',
                  'sort':'pub_date;-1'}
        results = filteredRetrieval(projectModel, params)
        
        # Should only be 3
        self.assertEquals(len(results), 3)
        order = [res.pub_date for res in list(results)][:5]

        # Get the time now as a starting point to difference backwards
        newer = datetime.datetime.utcnow()
        for ts in order:
            self.assertTrue(newer > ts)
            ts = newer
        
    def testFilterAndSort(self):
        ''' Tests against field filter and a sort'''

        params = {'effort':'1',
                  'sort':'importance;-1'}
        results = filteredRetrieval(projectModel, params)
        
        # Should be 5
        self.assertEquals(len(results), 5)
        order = [res.importance for res in list(results)][:5]

        maxImp = 6
        for imp in order:
            self.assertTrue(maxImp > imp)
            maxImp = imp

    def testFilterTagFilter1(self):
        ''' Tests against field filter and a tag filter'''

        params = {'effort':'1',
                  'tags':'homer,marge,bart'}
        results = filteredRetrieval(projectModel, params)
        self.assertEquals(len(results), 3)
        
    def testFilterTagFilter2(self):
        ''' Tests against field filter and a tag filter'''

        params = {'importance':'1',
                  'tags':'homer,marge,bart'}
        results = filteredRetrieval(projectModel, params)
        self.assertEquals(len(results), 1)
        
    # ------------------------------------------------------------
    # STITCHED ALL 3 TOGETHER
      
    def testTagsAndSortAndFieldFilter(self):
        ''' Tests against tag filter, field filter and a sort'''
 
        params = {'tags':'homer,marge,bart,moe',
                  'effort' : 1,
                  'sort': 'importance;-1'}
        results = filteredRetrieval(projectModel, params)
        
                # Should be 5
        self.assertEquals(len(results), 4)
        order = [res.importance for res in list(results)]

        maxImp = 6
        for imp in order:
            self.assertTrue(maxImp > imp)
            maxImp = imp
    