from django import forms
import sys
sys.path.append('..')
import ideasapp.settings as settings

class projectForm(forms.Form):
    
    title  = forms.CharField(widget=forms.TextInput(attrs={'placeholder':"Title?",'class':'span12'}))
    
    description = forms.CharField(required=True, max_length=200, widget=forms.Textarea(attrs={'placeholder':"What's will the project do",
                                                                                              'class':'span12'}))
    
    cls     = forms.ChoiceField(settings.CLASSIFICATIONS, required=True)
