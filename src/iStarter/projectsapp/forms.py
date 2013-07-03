from django import forms
import sys
sys.path.append('..')
import projectsapp.settings as settings

from ideasapp.models import idea as ideaModel
from taggit.forms import TagField

def get_idea_choices():
    return ideaModel.objects.values_list('id', 'title')

def get_rating_levels():
    ''' Gets the number of rating levels based on a settings param'''
    return [(i,i) for i in range(1, settings.PROJECT_RATING_LEVELS)]


class projectForm(forms.Form):
    
    def __init__(self, *args, **kwargs):
        super(projectForm, self).__init__(*args, **kwargs)
        self.fields['ideas'] = forms.MultipleChoiceField( choices=get_idea_choices(),
                                                          widget = forms.SelectMultiple(attrs={'class': 'span12',  # Make it same with as textare
                                                                                               'size': '16'} )) # make it 12 rows high
        
    title  = forms.CharField(widget=forms.TextInput(attrs={'placeholder':"Title?",'class':'span12'}))
    
    description = forms.CharField(required=True, max_length=200,
                                  widget=forms.Textarea(attrs={'placeholder': "What will the project do",
                                                               'class': 'span12',
                                                               'rows': '20'}))
    
    cls     = forms.ChoiceField(settings.CLASSIFICATIONS, required=True)

    #  These are the tags that a user entered manually
    new_tags = TagField(required=False, widget=forms.TextInput(attrs={'placeholder':"Add your own tags",'class':'span12', 'style':'margin:10px auto 10px auto;'}))
    
    # These are the tags we presented to them and they clicked on
    existing_tags = forms.CharField(required=False, widget=forms.HiddenInput)
    
    # To enable project scoring metrics
    importance_level = forms.IntegerField(widget=forms.Select(attrs={'style':'center-align:true;'},
                                                              choices=get_rating_levels()), required=True)
    effort_level     = forms.IntegerField(widget=forms.Select(choices=get_rating_levels()), required=True)
    resource_level   = forms.IntegerField(widget=forms.Select(choices=get_rating_levels()), required=True)
