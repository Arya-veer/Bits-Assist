
from django.contrib import admin
from django.urls import path, include
from query.views import *
from django.contrib.auth.views import LogoutView
from users import views as users_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', PostListView.as_view(),name='home_page'),
    path('post/<int:pk>/', CommentCreateView,name='comment_create'),
    path('post/new/',PostCreateView.as_view(),name='post_create'),
    path('accounts/', include('allauth.urls')),
    path('logout/', LogoutView.as_view(),name='signout'),
    path('profile/',users_views.profile,name='profile'),
    path('report/list/',ReportListView,name='report_list'),
    path('post/<int:pk>/report', reportconfirmview, name='report_confirm'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name='post_delete'),
    path('search_venues/', search_venues, name='search-venues'),
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)