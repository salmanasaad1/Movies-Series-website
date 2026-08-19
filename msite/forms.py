from django import forms
from django.contrib.auth.models import User
from .models import Userprofile

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    username=forms.CharField(help_text='      ')
    class Meta:
        model = User
        fields = [ 'username','email']
        widgets={
            'username':forms.TextInput(attrs={'class':'profile-tab-nav border-right'}),
            'email':forms.TextInput(attrs={'class':'em'})
        }
        

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Userprofile
        fields = [ 'image']