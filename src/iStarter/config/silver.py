"""    settings for running on grunt.    """

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
     ('Rich Brantingham', 'brantinr@ptn.dstl.uk.vl'),
)

# Email Settings
EMAIL_PORT = 25
EMAIL_HOST = 'mailhost.ptn.dstl.uk.vl'
FEEDBACK_RECIPIENTS = ['brantinr@ptn.dstl.uk.vl',]

# ELASTICSEARCH
DBHOST = 'http://localhost'
USER     = '<username>'
PASSWORD = '<password>'

# MONGO
MONGO_HOST = 'localhost'
MONGO_USER = 'search_admin'
MONGO_PSWD = 'search_4dmin'

# SEARCH API URL
API_URL = 'http://25.128.234.166:8003/api/v1/?'

# FEEDBACK DB PARAMETERS - THIS IS MONGO TOO
FEEDBACK_USER = 'search_admin'
FEEDBACK_PSWD = 'search_4dmin'

# URL OF GET DOCS SERVICE
GETDOCS = 'http://dev.dstl.uk.vl/getdoc?docid='
