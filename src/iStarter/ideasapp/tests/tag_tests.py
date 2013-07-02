"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
import os
import datetime
import random
import copy
import operator
from django.test import TestCase
from ideasapp.models import idea as ideaModel
from ideasapp.code import distinctTagsSortedAlpha, distinctTagsSortedCount

class TestTagModel(TestCase):
    
    def setUp(self):
        ''' Build the necessary data'''

        # Instantiate idea
        self.idea = ideaModel(idea_title="great idea",
                         pub_date=datetime.datetime.utcnow(),
                         idea_text="here's a great idea",
                         num_backers=1,
                         idea_classification="unclassified",
                         idea_headers="headers here;and here")
        self.idea.save()
        
        # Get hold of some test words
        testsPath = os.path.dirname(os.path.abspath(__file__))
        nouns = open(os.path.join(testsPath, 'resource_nouns.txt'), 'r')
        self.words = [line.replace('\r\n', '') for line in nouns.readlines()]

        # Put every 50th word into a list (cross section of start letters)         
        self.orderedWords = [self.words[i] for i in range(0,len(self.words)-1, 50)]
        self.shuffleWords = copy.copy(self.orderedWords)

        # Jumble the words into a new list
        random.shuffle(self.shuffleWords)
        
        # Save them against the current object
        for sWord in self.shuffleWords:
            self.idea.tags.add(sWord)
        self.idea.save()
        
#----------------------------------------------------------------------------------------

    def tearDown(self):
        ''' Delete all the items'''
        
        ideaModel.objects.all().delete()
        
#----------------------------------------------------------------------------------------
    
    def distinctTagsSortedAlpha(self):
        """
        tests that the tags coming back are distinct
        """
        
        dTags = distinctTagsSortedAlpha()
        self.assertEquals(dTags, self.orderedWords)

#----------------------------------------------------------------------------------------
    
    def testdistinctTagsSortedCount(self):
        """
        Test function to produce list of count, then alphabetically sorted tags 
        """
        
        # Create another idea to assign tags to
        idea = ideaModel(idea_title="great idea 2",
                         pub_date=datetime.datetime.utcnow(),
                         idea_text="here's another great idea",
                         num_backers=1,
                         idea_classification="unclassified",
                         idea_headers="headers here;and here")
        idea.save()

        # Create a list that contains all of the ordered words and their initial count        
        counts = [[wd, 1] for wd in self.orderedWords]
        
        # Loop through the first 10 items in the ordered list and add a tag
        for i in range(20):
            word = self.orderedWords[i]
            idea.tags.add(word)
            idea.save()
            
            for x in range(len(counts)-1):
                if counts[x][0] == word:
                    counts[x][1] += 1
            
        counts.sort(key=operator.itemgetter(1), reverse=True)
        
        # Call function
        countSortedTags = distinctTagsSortedCount()
        self.assertEquals(countSortedTags, counts)    
            
            
            
        
