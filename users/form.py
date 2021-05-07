from django.contrib.auth.models import User
from django import forms

from .models import profile



class Users_updateprofile_forms(forms.ModelForm):
        email = forms.EmailField(required=False)


        class Meta:
            model = User
            fields = ['username', 'email', ]

class dp_update_form(forms.ModelForm):
    class Meta:
        model = profile
        fields = ['image']