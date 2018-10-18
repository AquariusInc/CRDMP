from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import MyUser

class SignUpForm(UserCreationForm):
    dob = forms.DateField(help_text='Required. Format: YYYY-MM-DD')
    first_name = forms.CharField(help_text='Required')
    last_name = forms.CharField(help_text='Required')
    branchID = forms.IntegerField(label='Branch ID', help_text='Required')
    is_management = forms.BooleanField(label='Management Staff', help_text='BUGGED', initial=False, required=False)
    
    class Meta:
        model = MyUser
        fields = ('username', 'dob', 'first_name', 'last_name', 'is_management', 'branchID', 'password1', 'password2' )
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user