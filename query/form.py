from django.contrib.auth.models import User
from django import forms
from .models import comments


class CommentcreateForm(forms.ModelForm):


    class Meta:
        model = comments
        fields = ['comment']


