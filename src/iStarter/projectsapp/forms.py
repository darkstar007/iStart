from django import forms
import sys
sys.path.append('..')
import ideasapp.settings as settings
from ideasapp.models import idea as ideaModel
from taggit.forms import TagField

def get_idea_choices():
    return ideaModel.objects.values_list('id', 'title')


class projectForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(projectForm, self).__init__(*args, **kwargs)
        self.fields['ideas'] = forms.MultipleChoiceField( choices=get_idea_choices(),
                                                          widget = forms.SelectMultiple(attrs={'class': 'span12',  # Make it same with as textare
                                                                                               'size': '14'} )) # make it 12 rows high

 
    title  = forms.CharField(widget=forms.TextInput(attrs={'placeholder':"Title?",'class':'span12'}))
    
    description = forms.CharField(required=True, max_length=200,
                                  widget=forms.Textarea(attrs={'placeholder': "What will the project do",
                                                               'class': 'span12'}))
    
    cls     = forms.ChoiceField(settings.CLASSIFICATIONS, required=True)

    #  These are the tags that a user entered manually
    new_tags = TagField(required=False, widget=forms.TextInput(attrs={'placeholder':"Add your own tags",'class':'span12'}))
    
    # These are the tags we presented to them and they clicked on
    existing_tags = forms.CharField(required=False, widget=forms.HiddenInput)