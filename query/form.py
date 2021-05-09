from django.contrib.auth.models import User
from django import forms
from .models import *


class CommentcreateForm(forms.ModelForm):


    class Meta:
        model = comments
        fields = ['comment']

class RatingForm(forms.ModelForm):


    class Meta:
        model = Rating
        fields=['rating']


