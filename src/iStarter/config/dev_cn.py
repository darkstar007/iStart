"""    settings for running on Chris Nich's home machine.    """

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
     ('Rich Brantingham', 'brantinr@ptn.dstl.uk.vl'),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'dusted',                      # Or path to database file if using sqlite3.
        'USER': 'dusted',                      # Not used with sqlite3.
        'PASSWORD': 'dusted',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}