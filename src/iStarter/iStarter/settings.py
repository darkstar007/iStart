#////////////////////////////////////////////////////////////////////////////////////
#
# This settings file adds in other settings files that are based on the 
# local running environment - the mac, dev server and deployments.
#
# Then each app has a number of settings, which are unique to them. They 
# import this settings file (and hence the local bits) and then extend
# with the app-based settings.
#
# Some of the settings in this file are only used by 2 or so apps, so they
# will need to be transferred with the app if it gets used elsewhere.
#
#
#////////////////////////////////////////////////////////////////////////////////////



import os

#////////////////////////////////////////////////////////////////////////////////////
#
#    METHOD USED FOR ACCESSING MACHINE SPECIFIC SETTINGS (SEE config FOLDER AT PROJECT ROOT)
#
#////////////////////////////////////////////////////////////////////////////////////

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# You can key the configurations off of anything - I use project path.
configs = {
    '/Users/brantinghamr/Documents/Code/eclipseWorkspace/iStart/src/iStarter'   : 'dev_rb',
    '/Users/darren/Development/iStart/src/iStarter'                                : 'dev_dm',
    '/home/dusted/git/iStart/src/iStarter'                                : 'dev_cn',
    'PREPEND YOUR PATH HERE/iStart/src/iStarter'                                : 'dev_mn',

    'PREPEND YOUR PATH HERE/iStart/src/iStarter'                                : 'dotcloud',
    'PREPEND YOUR PATH HERE/iStart/src/iStarter'                                : 'silver',
}

# Import the configuration settings file - REPLACE projectname with your project
config_module = __import__('config.%s' % configs[ROOT_PATH], globals(), locals(), 'iStarter')

# Load the config settings properties into the local scope.
for setting in dir(config_module):
    if setting == setting.upper():
        locals()[setting] = getattr(config_module, setting)

# ADMINS SHOULD BE ACCESSIBLE FROM THE CONFIG FILES
MANAGERS = ADMINS

#////////////////////////////////////////////////////////////////////////////////////
#
#    PROJECT WIDE DATABASE SETTINGS
#
#////////////////////////////////////////////////////////////////////////////////////


# This used for TESTS
'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'istarter',                                 # Or path to database file if using sqlite3.
        'USER': 'django_usr',                               # Not used with sqlite3.
        'PASSWORD': 'django_usr',                           # Not used with sqlite3.
        'HOST': 'localhost',                                # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                                         # Set to empty string for default. Not used with sqlite3.
    }
}
'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    
        'NAME': '/home/dusted/istarter.sqlite3'
    }
}


#////////////////////////////////////////////////////////////////////////////////////
#
#    SECURITY BANNER SETTINGS
#
#////////////////////////////////////////////////////////////////////////////////////

# Needed in searchstatic app and searchapp

SECURITY_BANNER = "  --   PROTOTYPE"

CLASSIFICATION_RANK = ['unknown',
                       'unclassified',
                       'restricted',
                       'confidential',
                       'secret',
                       'top secret']


#////////////////////////////////////////////////////////////////////////////////////
#
#    PROJECT WIDE LOGGING
#
#////////////////////////////////////////////////////////////////////////////////////

# Whether to log searches or not - this is handled differently, but should probably be handled with a logging handler.
LOG_SEARCHES = True

# Additional locations of static files
logFile        = "istarter_error.log"
requestLogFile = "istarter_requests.log"

LOG_PATH = os.path.join(ROOT_PATH, 'logs')

# LOG_PATH is pulled from the local settings files
LOG_FILE_PATH    = os.path.join(LOG_PATH, logFile)
REQUEST_LOG_PATH = os.path.join(LOG_PATH, requestLogFile)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level':'WARNING',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': LOG_FILE_PATH,
            'maxBytes': 1024*1024*5, # 5 MB
            'backupCount': 5,
            'formatter':'standard',
        },  
        'request_handler': {
                'level':'DEBUG',
                'class':'logging.handlers.RotatingFileHandler',
                'filename': REQUEST_LOG_PATH,
                'maxBytes': 1024*1024*5, # 5 MB
                'backupCount': 5,
                'formatter':'standard',
        },
    },
    'loggers': {

        '': {
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': True
        },
        'django.request': {
            'handlers': ['request_handler'],
            'level': 'DEBUG',
            'propagate': False
        },
    }
}


#////////////////////////////////////////////////////////////////////////////////////
#
#    INFREQUENTLY CHANGED DEFAULT SETTINGS PROJECT WIDE
#
#////////////////////////////////////////////////////////////////////////////////////

TEMPLATE_DIRS = (os.path.join(ROOT_PATH, 'templates'),)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ideasapp',
    #'accountsapp',
    # Uncomment the next line to enable the admin:
    # 'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

TIME_ZONE = 'Europe/London'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-uk'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'ytqsffdhs2v*4y)+t$p*2g_#+)rgh*si1eq0qnt1wr%afx$r^z'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'iStarter.urls'

