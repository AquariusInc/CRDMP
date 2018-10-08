from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import MyUser

class SignUpForm(UserCreationForm):
    dob = forms.DateField(help_text='Required. Format: YYYY-MM-DD')
    firstName = forms.CharField(help_text='Required')
    lastName = forms.CharField(help_text='Required')
    branchID = forms.IntegerField()
   
    class Meta:
        model = MyUser
        fields = ('username', 'dob', 'firstName', 'lastName', 'branchID', 'password1', 'password2', )