from django import forms
import sys
sys.path.append('..')
import ideasapp.settings as settings
from ideasapp.models import idea as ideaModel

def get_idea_choices():
    return ideaModel.objects.values_list('id', 'title')


class projectForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(projectForm, self).__init__(*args, **kwargs)
        self.fields['ideas'] = forms.MultipleChoiceField( choices=get_idea_choices() )

 
    title  = forms.CharField(widget=forms.TextInput(attrs={'placeholder':"Title?",'class':'span12'}))
    
    description = forms.CharField(required=True, max_length=200,
                                  widget=forms.Textarea(attrs={'placeholder': "What's will the project do",
                                                               'class': 'span12'}))
    
    cls     = forms.ChoiceField(settings.CLASSIFICATIONS, required=True)

