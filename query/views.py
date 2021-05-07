from django.shortcuts import render, redirect
from django.views.generic import DetailView, CreateView, DeleteView,ListView
from .form import CommentcreateForm
from django.contrib.auth.decorators import login_required
from .models import posts, comments
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from Bits_queries.settings import LOGIN_REDIRECT_URL
from django.contrib import messages



class PostListView(ListView):
    model= posts
    template_name = 'query/home.html'
    context_object_name='posts'
    ordering=['-rating']

class PostDetailView(DetailView):
    model=posts
    template_name = 'query/posts.html'
    context_object_name = 'posts'

class PostCreateView(CreateView):
    model=posts
    fields = ['title','content']
    template_name = 'query/posts_form.html'

    def form_valid(self, form):
        form.instance.writer=self.request.user
        return super().form_valid(form)

# class CommentCreateView(CreateView):
#     model=comments
#     fields = ['comment']
#     template_name = 'query/posts.html'
#     context_object_name = 'form'
#     extra_context = {'object'}
#
#
#     def form_valid(self, form):
#         current_post=posts.objects.get(id=self.kwargs.get('pk'))
#         form.instance.writer=self.request.user
#         form.instance.post=current_post
#         return super().form_valid(form)

def CommentCreateView(request, **kwargs):
        current_post=posts.objects.filter(id=kwargs['pk'])[0]
        post_comments = comments.objects.filter(post=current_post).all()
        post_rating = current_post.rating
        post_times_rated = current_post.times_rated

        # avg_rating=post_comments.ratings
        if request.method=='POST':
            rating = request.POST.get("rated")
            if rating is not None:
                current_post.rating = (int(rating)+(post_rating*post_times_rated))/(post_times_rated+1)
                current_post.times_rated = post_times_rated+1
                current_post.save()
            form=CommentcreateForm(request.POST)
            if form.is_valid():
                form.instance.writer=request.user
                form.instance.post=current_post
                form.save()
            return redirect('home_page')


        else:
            form = CommentcreateForm
            context={
                'form': form,
                'post': current_post,
                'comments': post_comments,
            }
            return render(request, 'query/posts.html', context)

# class ReportListView(ListView):
#     model= posts
#     template_name = 'query/report_list.html'
#     context_object_name='reports'


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