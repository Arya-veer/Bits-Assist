# from django import template
# from allauth.socialaccount.models import SocialAccount
# from django.contrib.auth.models import User
# register=template.Library()
#
# @register.simple_tag
# def get_loggedin_data(id):
#     current_user=User.objects.filter(id=id).first()
#     extradata=SocialAccount.objects.filter(user=current_user).first().extra_data
#     if "hd" in extradata.keys():
#         x=1
#     else:
#         x=0
#     return x

