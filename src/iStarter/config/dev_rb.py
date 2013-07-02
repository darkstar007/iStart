"""    settings for running on RB's home machine.    """

"""    settings for running on Matt's home machine.    """

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
     ('Rich Brantingham', 'rich.brantingham@me.com'),
)


#Set this to true to load data - false to not
testDataChk = True
#Paths for where the nouns file and header data file is stored
testDataPath = r'/Users/robrant/eclipseCode/istarter/iStart/src/iStarter/config'
nounsfile = 'nouns.txt'
headersfile = 'example_headers.txt'

#Apps that have models for loading of data
testDataAppsList = ['ideasapp', 'projectsapp']
#Number of rows to add
testDataNumRows = 500
#Path to where fixutres file will be saved - this should be accessible really
#as its always in the fixtures directory under app
fixtureOutPath = r'/Users/robrant/eclipseCode/istarter/iStart/src/iStarter/'
fixtureDateFname = 'initial_data.json'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'istarter',                                 # Or path to database file if using sqlite3.
        'USER': 'postgres',                               # Not used with sqlite3.
        'PASSWORD': 'postgres',                           # Not used with sqlite3.
        'HOST': 'localhost',                                # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                                         # Set to empty string for default. Not used with sqlite3.
    }
}


DEBUG = True
TEMPLATE_DEBUG = DEBUG


#EMAIL_HOST_USER     = 'brantinghamr@hotmail.com'
#EMAIL_HOST_PASSWORD = '*******'
#EMAIL_PORT          = 587
#EMAIL_HOST          = 'smtp.live.com'
#EMAIL_USE_TLS       = True
#FEEDBACK_RECIPIENTS = ['rich.brantingham@me.com',]
