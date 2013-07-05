'''
Store project scoring algorithms in here
'''

def noddy(importance, resource, effort):
    ''' Adds the 3 scores together - placeholder '''
    
    score = importance * resource * effort
    return score

#------------------------------------------------------

def backersRequiredAlgorithm(effort, importance, resources) :        
    #------------------------------------------------------------------------
    # code to calculate the numbr of backers required before a project is taken on
    #
    #    effort         : The amount of effort reuired to complete the project (1-5)
    #        It might require a lot of software design, or development of a new algorithm
    #                This is really a measure of manpower requirements
    #   importance     : How important is it that the project gets taken on (1-5)
    #         This could reflect the national priority framework or it might be 
    #        that other initiatives cannot be taken on until this is completed
    #    resources    : How many extra resources are required to achived the projects goals (1-5)
    #        This are things that cost money Examples are: needs a new computer; needs 
    #         software purchasing; needs new paperclips
    #
    
    return effort * ((6-importance)**2) * (resources**3)
