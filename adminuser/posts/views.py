from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from flask import request
from .models import *
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.urls import reverse_lazy, reverse
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

def home(request):
    return render(request, 'posts/home.html')


def ddd(request):
    return render(request, 'posts/ddd.html')


@login_required
def user_page(request):
    i = request.user.pk
    p = Post.objects.filter(author__pk=i)
    return render(request, 'posts/user_page.html', {'post_list':p})


class PostDetailView(DetailView):
    model = Post


def following(request, kk):
    follow = User.objects.get(pk=kk)
    print(follow)
    followed = request.user
    print(followed)

    f1 = Twitter.objects.filter(follow=follow, followed=followed)
    print(f1)
    f1.delete()
    return redirect(reverse("posts:twitter"))


def followed(request):
    i = request.user.pk
    print(i)
    f1 = Twitter.objects.filter(followed__pk=i)

    return render(request, 'posts/twitter_list.html', {'twitter_list':f1})


class FollowListView(LoginRequiredMixin, ListView):
    login_url = '/user/login/'
    template_name = 'posts/follow_list.html'

    def get_queryset(self):
        return Twitter.objects.filter(follow=self.request.user)


def follow_unique(request):
    message = ''
    follow_pk = request.POST['follow']
    print(follow_pk)
    foolowed_pk = request.user.pk
    (foolowed_pk)
    post_list = Post.objects.filter(author__pk=follow_pk)
    if Twitter.objects.filter(follow=follow_pk, followed=foolowed_pk):
        message = 'Already follower'
    else:
        follow = User.objects.get(pk=request.POST['follow'])
        follower = request.user
        f1 = Twitter(follow=follow, followed=follower)
        f1.save()
    # return HttpResponseRedirect(reverse('posts:posts'))
    # return HttpResponseRedirect(reverse('posts:posts', kwargs={'message':message}))
    return render(request, 'posts/post_list.html', {'post_list':post_list, 'message':message})


class PostListView(ListView):
    model = Post
    paginate_by = 2

    def get_queryset(self):
        phrase_q = Q()
        q = self.request.GET.get('phrase')
        qa = self.request.GET.get('qa')
        if q:
            phrase_q &= (Q(title__icontains=q) | Q(title__icontains=q) | Q(title__icontains=q))
        if qa:
            phrase_q &= (Q(author__pk=qa))
        return Post.objects.filter(phrase_q).order_by('-pk')

def post_add(request):
    form = PostModelForm()
    if request.method == 'POST':
        if request.user:
            form = PostModelForm(request.POST, request.FILES)
            # print(form)
            if form.is_valid():
                postm = form.save(commit=False)
                # print(postm)
                postm.author = request.user
                # postm.author = User.objects.get(pk=request.user.pk)
                postm.save()
                # კარგია თუ დამამახსოვრდება, სხვა დროსაც დამჭირდება
                # form.save_m2m()
                return redirect(reverse("posts:posts"))
    return render(request, 'posts/post_form.html', {'form':form})


class PostCreateView(CreateView):
    fields = '__all__'
    model = Post


# აქ გვინდა რომ მხოლოდ პოსტის ავტორს შეეძლოს მოხვედრა
class PostUpdateView(UpdateView):
    fields = ('title', 'text', 'image')
    model = Post


# ეს არ შლის სურათს მედია ფაილიდან. გადასაწყვეტია ...
class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('posts:posts')