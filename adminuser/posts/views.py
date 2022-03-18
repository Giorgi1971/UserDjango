from itertools import count
from pyexpat import model
from statistics import mode
from tkinter import TkVersion
from tkinter.messagebox import QUESTION
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

class PersonalDetailView(DetailView):
    model = get_user_model()
    template_name = 'account/personal_info.html'


@login_required
def user_page(request):
    i = request.user.pk
    p = Post.objects.filter(author__pk=i)
    return render(request, 'posts/user_page.html', {'post_list':p})


class ExampleListView(LoginRequiredMixin, ListView):
    # model = Post
    # extra_context={'title': 'Custom Title'}
    # # ქვერისეთი რა სახელით იქნება ტემპლატში
    context_object_name = 'list'
    template_name = 'posts/example2.html'
    # # თუ გვინდა რომ სხვა ობიექტის სია მოგვცეს
    # queryset  = User.objects.all()
     
    # def get_queryset(self):
    #     return Twitter.objects.filter(followed=self.request.user)

    # ახალი ვარიანტი
    def get_queryset(self):
        qf = Twitter.objects.filter(followed=self.request.user) # .annotate(tt=(follow__post_set=))
        tt = []
        for i in qf:
            p = i.follow.post_set.all()
            tt.extend(p)
        tk = [i.pk for i in tt]
        querset = Post.objects.filter(id__in=tk)
        return querset.order_by('?')



# ცალკეული პოსტის ნახვა, თუ ავტორი ნახულობს აქვს რედაქტირების საშუალება
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
    print(foolowed_pk)
    post_list = Post.objects.filter(author__pk=follow_pk).order_by()
    print(post_list)
    if Twitter.objects.filter(follow=follow_pk, followed=foolowed_pk):
        message = 'Already follower'
    else:
        follow = User.objects.get(pk=request.POST['follow'])
        follower = request.user
        f1 = Twitter(follow=follow, followed=follower)
        f1.save()
        message = f'follow {follow} follower'
    return render(request, 'posts/post_list.html', {'page_obj':post_list, 'message':message})


# პოსტების დაბრუნება, მათ შორის გაფილტრულისაც სათაურით და ტექსტსტით.
class PostListView(ListView):
    model = Post
    paginate_by = 2

    def get_queryset(self):
        phrase_q = Q()
        q = self.request.GET.get('phrase')
        qa = self.request.GET.get('qa')
        if q:
            phrase_q &= (Q(title__icontains=q) | Q(text__icontains=q) | Q(title__icontains=q))
        if qa:
            phrase_q &= (Q(author__pk=qa))
        print(self.request.user.pk)
        p1 = Post.objects.filter(phrase_q) #.filter(author__followed__pk=self.request.user.pk)
        return p1.order_by('-pk')

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