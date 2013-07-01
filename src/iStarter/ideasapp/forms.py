from django import forms
import ideasapp.settings as settings
from taggit.forms import TagField

class ideaForm(forms.Form):
    
    title  = forms.CharField(widget=forms.TextInput(attrs={'placeholder':"Title?",'class':'span12'}))
    
    description = forms.CharField(required=True, max_length=200, widget=forms.Textarea(attrs={'placeholder':"What's the idea?",
                                                                                              'class':'span12'}))
    
    cls     = forms.ChoiceField(settings.CLASSIFICATIONS, required=True)
    
    tags = TagField(widget=forms.TextInput(attrs={'placeholder':"Other tags?",'class':'span12'}))