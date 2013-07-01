"""    settings for running on Chris Nich's home machine.    """

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
     ('Rich Brantingham', 'brantinr@ptn.dstl.uk.vl'),
)


#Set this to true to load data - false to not
testDataChk = True
#Paths for where the nouns file and header data file is stored
testDataPath = r'/home/dusted/git/iStart/src/iStarter/config'
nounsfile = 'nouns.txt'
headersfile = 'example_headers.txt'

#Apps that have models for loading of data
testDataAppsList = ['ideasapp']
#Number of rows to add
testDataNumRows = 500
#Path to where fixutres file will be saved - this should be accessible really
#as its always in the fixtures directory under app
fixtureOutPath = r'/home/dusted/git/iStart/src/iStarter/'
fixtureDateFname = 'initial_data.json'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    
        'NAME': '/home/dusted/istarter.sqlite3'
    }
}



