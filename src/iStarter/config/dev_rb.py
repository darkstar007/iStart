"""    settings for running on RB's home machine.    """

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
     ('Rich Brantingham', 'brantinr@ptn.dstl.uk.vl'),
)


EMAIL_HOST_USER     = 'brantinghamr@hotmail.com'
EMAIL_HOST_PASSWORD = '*******'
EMAIL_PORT          = 587
EMAIL_HOST          = 'smtp.live.com'
EMAIL_USE_TLS       = True
FEEDBACK_RECIPIENTS = ['rich.brantingham@me.com',]
