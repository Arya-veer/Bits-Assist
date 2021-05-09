from django.contrib import admin
from .models import posts,comments,Rating


admin.site.register(posts)
admin.site.register(comments)
admin.site.register(Rating)
