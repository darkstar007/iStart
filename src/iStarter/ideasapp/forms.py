from django import forms
import ideasapp.settings as settings
from taggit.forms import TagField

class ideaForm(forms.Form):
    
    title  = forms.CharField(widget=forms.TextInput(attrs={'placeholder':"Title?",'class':'span12'}))
    
    description = forms.CharField(required=True, max_length=500, widget=forms.Textarea(attrs={'placeholder':"What's the idea?",
                                                                                              'class':'span12'}))
    
    cls     = forms.ChoiceField(settings.CLASSIFICATIONS, required=True)
    
    #  These are the tags that a user entered manually
    new_tags = TagField(widget=forms.TextInput(attrs={'placeholder':"Add your own tags",'class':'span12'}))
    
    # These are the tags we presented to them and they clicked on
    existing_tags = forms.CharField(required=False, widget=forms.HiddenInput)