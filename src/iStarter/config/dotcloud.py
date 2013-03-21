"""    settings for running on dotcloud.    """

# Get the sensitive information that isn't checked into github
from dotcloudSecrets import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
     ('Rich Brantingham', 'rich.brantingham@me.com'),
)

# Email settings - see also settings in dotcloudSecrets.py
#EMAIL_HOST_USER     = 'emailAddressInHere'
#EMAIL_HOST_PASSWORD = 'emailAddressPasswordInHere'
EMAIL_PORT          = 587
EMAIL_HOST          = 'smtp.live.com'
EMAIL_USE_TLS       = True
FEEDBACK_RECIPIENTS = ['rich.brantingham@me.com',]

# ELASTICSEARCH
DBHOST = 'http://localhost'
#USER     = '<ESusername>'
#PASSWORD = '<ESpassword>'

# MONGO
# MONGO
MONGO_HOST = 'localhost'
#MONGO_USER = 'mongoUser'
#MONGO_PSWD = 'mongoPswd'

# SEARCH API URL
API_URL = 'http://localhost:8003/api/v1/?'

# URL OF GET DOCS SERVICE
GETDOCS = 'http://***********/getdoc?docid='
