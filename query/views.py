from django.db.models import Sum, Avg
from django.shortcuts import render, redirect
from django.views.generic import DetailView, CreateView, DeleteView,ListView
from .form import *
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from Bits_queries.settings import LOGIN_REDIRECT_URL
from django.contrib import messages



class PostListView(ListView):
    model= posts
    template_name = 'query/home.html'
    context_object_name='posts'
    ordering=['-avg_rating']

class PostCreateView(CreateView):
    model=posts
    fields = ['title','content']
    template_name = 'query/posts_form.html'

    def form_valid(self, form):
        form.instance.writer=self.request.user
        return super().form_valid(form)


def CommentCreateView(request, **kwargs):
    current_post = posts.objects.filter(id=kwargs['pk'])[0]
    post_comments = comments.objects.filter(post=current_post).all()
    current_user=request.user
    post_rating=Rating.objects.filter(post=current_post).all()
    times_rated=post_rating.count()
    if times_rated==0:
        avg_rating=0
    else:
        avg_rating=post_rating.aggregate(Avg('rating'))['rating__avg']
    current_post.avg_rating=avg_rating
    current_post.times_rated=times_rated
    current_post.save()


    if request.method == 'POST':
        cform = CommentcreateForm(request.POST)
        rform = RatingForm(request.POST)




        if rform.is_valid():
            rform.instance.rater=request.user
            rform.instance.post = current_post
            rform.save()

        if cform.is_valid():
            cform.instance.writer = request.user
            cform.instance.post = current_post
            cform.save()
        return redirect('home_page')


    else:
        post_ratings = Rating.objects.filter(post=current_post).all()
        user_post_rating = post_ratings.filter(rater=current_user).all()
        if user_post_rating.exists():
            x = 1
        else:
            x = 0
        cform = CommentcreateForm
        rform = RatingForm
        context = {
            'cform': cform,
            'rform': rform,
            'post': current_post,
            'comments': post_comments,
            'x':x,
        }
        return render(request, 'query/posts.html', context)



def ReportListView(request):
    current_user=request.user
    if current_user.is_authenticated:
        reports = posts.objects.filter(report=True)
        if current_user.is_superuser:
            context={
                'posts': reports
            }
            return render(request, 'query/report_list.html', context)
        else:
            raise PermissionDenied

    else:
        return redirect('signout')

def reportconfirmview(request, **kwargs):
    current_post = posts.objects.filter(id=kwargs['pk'])[0]
    if request.method=='POST':
        current_post.report = True
        current_post.save()
        messages.warning(request, f'Reported')
        return redirect('home_page')
    else:
        context={
            'post': current_post
        }
        return render(request, 'query/confirm_report.html', context)

class PostDeleteView(DeleteView):
    model = posts
    template_name = 'query/post_delete_confirm.html'
    context_object_name = 'post'
    success_url = '/report/list/'

def search_venues(request):
    if request.method == 'POST':
        searched = request.POST.get("searched")
        post = posts.objects.filter(title__contains=searched)|posts.objects.filter(content__contains=searched)
        context={
            'searched': searched,
            'posts': post,
        }
    return render(request, 'query/search_venues.html', context)