# from django.core.serializers import json/
import json

from django.shortcuts import render,redirect
from django.contrib import messages
from .form import Users_updateprofile_forms,dp_update_form
from django.contrib.auth.decorators import login_required
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import User







@login_required
def profile(request):

    current_user = request.user
        #User.objects.filter(id=request.user.id).first()
    extradata = SocialAccount.objects.filter(user=current_user).first().extra_data
    img = extradata["picture"]

    if request.method == 'POST':
       u_form = Users_updateprofile_forms(request.POST,instance=request.user)
       p_form = dp_update_form(request.POST,request.FILES,instance=request.user.profile)
       if u_form.is_valid() and p_form.is_valid():
           u_form.save()
           p_form.save()
           messages.success(request,f'account has been updated ')
           return redirect('home_page')

    else:
       u_form = Users_updateprofile_forms(instance=request.user)
       p_form = dp_update_form(instance=request.user.profile)

    context = {
    'p_form': p_form,
    'u_form': u_form,
    'img':img,
    }

    return render(request,'users/profile.html',context)