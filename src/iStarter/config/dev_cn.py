"""    settings for running on Chris Nich's home machine.    """

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
     ('Rich Brantingham', 'brantinr@ptn.dstl.uk.vl'),
)

#Paths for where the nouns file is stored
testDataPath = r'/home/dusted/git/iStart/src/iStarter/config'
nounsfile = 'nouns.txt'
headersfile = 'example_headers.txt'

#flag for whether to do the data load
testDataLoad = True
#Apps that have models for loading of data
testDataAppsList = ['ideasapp']
#Number of rows to add
testDataNumRows = 50

