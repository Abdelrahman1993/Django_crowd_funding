from django import forms
from taggit.forms import *


class CreateProject(forms.Form):
    Title = forms.CharField(label="Title", required="true", min_length=10, max_length=100,
                            widget=forms.TextInput(attrs={'class': 'col-12 btn-lg'}))
    Details = forms.CharField(label="Details", required="true", min_length=10, max_length=100,
                              widget=forms.Textarea(attrs={'class': 'col-12 btn-lg', 'rows': 3}))
    category = forms.CharField(label="category", required="true", min_length=10, max_length=200,
                               widget=forms.TextInput(attrs={'class': 'col-12 btn-lg'}))
    Total_target = forms.CharField(label="Total target", required="true", min_length=10, max_length=200,
                                   widget=forms.TextInput(attrs={'class': 'col-12 btn-lg'}))
    Tags = TagField(label="Tags", required="true", min_length=10, max_length=100,
                    widget=forms.TextInput(attrs={'class': 'col-12 btn-lg'}))
    image = forms.ImageField()
