from django import forms
from django.forms import ModelForm 
from .models import Project, Task
from django.core.exceptions import ValidationError  
from django.contrib.auth.forms import UserCreationForm  
from django.contrib.auth.models import User  

class CreateNewTask(forms.Form):
    title = forms.CharField(label="Title", max_length=200, widget=forms.TextInput(attrs={"class": "input"}))
    description = forms.CharField(label="Description", required=False, widget=forms.Textarea(attrs={"class": "input"}))
    project = forms.ModelChoiceField(queryset=Project.objects.all(),label="Project", empty_label=None, widget=forms.Select(attrs={"class": "input"}))
    important = forms.BooleanField(label="Important")
    
class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ("title", "description", "project", "important")

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ("name",)
        
class CreateNewProject(forms.Form):
    name = forms.CharField(label="Name", max_length=200, widget=forms.TextInput(attrs={"class": "input"}))

class CustomUserCreationForm(UserCreationForm):  
    username = forms.CharField(label='username', min_length=5, max_length=150)  
    email = forms.EmailField(label='email')  
    password1 = forms.CharField(label='password', widget=forms.PasswordInput)  
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)  
  
    def username_clean(self):  
        username = self.cleaned_data['username'].lower()  
        new = User.objects.filter(username = username)  
        if new.count():  
            raise ValidationError("User Already Exist")  
        return username  
  
    def email_clean(self):  
        email = self.cleaned_data['email'].lower()  
        new = User.objects.filter(email=email)  
        if new.count():  
            raise ValidationError(" Email Already Exist")  
        return email  
  
    def clean_password2(self):  
        password1 = self.cleaned_data['password1']  
        password2 = self.cleaned_data['password2']  
  
        if password1 and password2 and password1 != password2:  
            raise ValidationError("Password don't match")  
        return password2  
  
    def save(self, commit = True):  
        user = User.objects.create_user(  
            self.cleaned_data['username'],  
            self.cleaned_data['email'],  
            self.cleaned_data['password1']  
        )  
        return user  