from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import MyUser

class SignUpForm(UserCreationForm):
    dob = forms.DateField(help_text='Format: YYYY-MM-DD')
    first_name = forms.CharField(help_text='Required')
    last_name = forms.CharField(help_text='Required')
    staffID = forms.IntegerField(label='Staff ID', help_text='Required', initial=0)
    branchID = forms.IntegerField(label='Branch ID', help_text='Required', initial=0)
    is_management = forms.BooleanField(label='Management Staff', initial=False, required=False)
    
    class Meta:
        model = MyUser
        fields = ('username', 'dob', 'first_name', 'last_name', 'is_management', 'staffID', 'branchID', 'password1', 'password2' )