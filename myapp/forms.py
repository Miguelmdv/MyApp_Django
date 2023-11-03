from django import forms
from .models import Project

class CreateNewTask(forms.Form):
    title = forms.CharField(label="Title", max_length=200, widget=forms.TextInput(attrs={"class": "input"}))
    description = forms.CharField(label="Description", required=False, widget=forms.Textarea(attrs={"class": "input"}))
    project = forms.ModelChoiceField(queryset=Project.objects.all(),label="Project", empty_label=None, widget=forms.Select(attrs={"class": "input"}))
    
class CreateNewProject(forms.Form):
    name = forms.CharField(label="Name", max_length=200, widget=forms.TextInput(attrs={"class": "input"}))