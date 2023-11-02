from django import forms

class CreateNewTask(forms.Form):
    title = forms.CharField(label="Title", max_length=200)
    description = forms.CharField(label="Description", required=False, widget=forms.Textarea())
    
class CreateNewProject(forms.Form):
    name = forms.CharField(label="Name", max_length=200)