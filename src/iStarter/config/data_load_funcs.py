# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 09:25:23 2013

@author: dusted

Functions for making test data for database
This wont include the actual load yet
"""
from datetime import datetime
from random import randint
#Uncmment this when deplpoyed with django
#import ideasapp.settings as dataloadsettings


class testData():
    def __init__(self):   
    #Paths for where the nouns file is stored
        self.nounspth = r'/home/dusted/git/iStart/src/iStarter/config'
        self.nounsfile = 'nouns.txt'
        print 'Loading test data'
        fh = open(self.nounspth+'/'+self.nounsfile,'r')
        self.words = []
        while fh.readline():
            self.words.append(fh.readline().rstrip('\r\n'))
        fh.close()
    
    def randomDate(self):
        #Makes Random date
        dtg = datetime(randint(2012,2015),randint(1,12),randint(1,28),randint(0,23),randint(0,59),randint(0,59))
        return dtg
    
    def randomText(self,chars):
        #Makes random text - chars is the number of characters allow max
        #Can be used for titles or body text etc
        #print 'Loading test data'
        #fh = open(self.nounspth+'/'+self.nounsfile,'r')
        #words = []
        #fh.close()
        #Load into a list
        #while fh.readline():
        #    words.append(fh.readline().rstrip('\r\n'))
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
        #fh = open(self.nounspth+'/'+self.nounsfile,'r')
        #words = []
        #fh.close()
        email = names[randint(0,len(names))]+'@'+self.words[randint(0,len(self.words))]+'.com'
        return email
    
if __name__ == "__main__":
    r = testData()
    print r.randomDate()
    print r.randomText(200)
    print r.randomEmail()
    
