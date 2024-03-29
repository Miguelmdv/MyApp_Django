from django import forms
from django.forms import ModelForm
from .models import Project, Task
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import re


class TaskForm(ModelForm):
    def __init__(self, *args, **kwargs):
        projects_user = kwargs.pop("projects_user", None)
        super(TaskForm, self).__init__(*args, **kwargs)
        if projects_user:
            self.fields["project"].queryset = projects_user

    class Meta:
        model = Task
        fields = ("title", "description", "project", "important")


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ("name",)


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(label="username", min_length=3, max_length=150)
    email = forms.EmailField(label="email")
    password1 = forms.CharField(label="password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm password", widget=forms.PasswordInput)

    def username_clean(self):
        username = self.cleaned_data["username"].lower()
        new = User.objects.filter(username=username)
        if new.count():
            raise ValidationError("User Already Exist")
        return username

    def email_clean(self):
        email = self.cleaned_data["email"].lower()
        new = User.objects.filter(email=email)
        if new.count():
            raise ValidationError("Email Already Exist")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data["password1"]
        password2 = self.cleaned_data["password2"]

        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")
        return password2

    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data["username"],
            self.cleaned_data["email"],
            self.cleaned_data["password1"],
        )
        return user
