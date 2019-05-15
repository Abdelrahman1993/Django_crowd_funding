from django import forms
from taggit.forms import *
from .models import Project


class CreateProject(forms.Form):
    title = forms.CharField(label="Title", required=True, min_length=10, max_length=100,
                            widget=forms.TextInput(attrs={'class': 'col-12 btn-lg'}))
    target = forms.IntegerField(label="target", required=True, min_value=1000, max_value=1000000)
    details = forms.CharField(label="Details", required=True, min_length=10, max_length=100,
                              widget=forms.Textarea(attrs={'class': 'col-12 btn-lg', 'rows': 3}))
    category = forms.ChoiceField(label="category", required=True,
                                 widget=forms.TextInput(attrs={'class': 'col-12 btn-lg'}))
    endTiem = forms.DateTimeField(label="end time", required=True,
                                  widget=forms.DateTimeInput(attrs={'type': 'date', 'class': 'col-12 btn-lg'}))
    tages = TagField(label="Tags", required="true",
                     widget=forms.TextInput(attrs={'class': 'col-12 btn-lg'}))
    Images = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))


# class UploadImages(forms.Form):
#     Images = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
