"""    settings for running on Darren's home machine.    """

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
          ('Rich Brantingham', 'brantinr@ptn.dstl.uk.vl'),
          )


#Set this to true to load data - false to not
testDataChk = True
#Paths for where the nouns file and header data file is stored
testDataPath = r'/Users/darren/Development/iStart/src/iStarter/config'
nounsfile = 'nouns.txt'
headersfile = 'example_headers.txt'

#Apps that have models for loading of data
testDataAppsList = ['ideasapp', 'projectsapp']
#Number of rows to add
testDataNumRows = 20
#Path to where fixutres file will be saved - this should be accessible really
#as its always in the fixtures directory under app
fixtureOutPath = r'/Users/darren/Development/iStart/src/iStarter/'
fixtureDateFname = 'initial_data.json'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/Users/darren/Development/istarter.sqlite3'
}
}


