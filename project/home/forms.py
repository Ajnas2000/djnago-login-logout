from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth.models import User
from django import forms

class RegisterUsere(UserCreationForm):
    class Meta:
        model=User
        fields=['username','email','password1','password2','is_superuser']

        
class EditForm(UserChangeForm):
    password=None
    class Meta:
        model=User
        fields=['username','email']
        widgets={
            'username':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'})
        }
















