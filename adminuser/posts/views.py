from django.shortcuts import render
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from .models import *
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q



def home(request):
    return render(request, 'posts/home.html')


def ddd(request):
    return render(request, 'posts/ddd.html')


@login_required
def user_page(request):
    return render(request, 'posts/user_page.html')


class PostView(ListView):
    model = Post
    paginate_by = 5

    def get_queryset(self):
        phrase_q = Q()
        q = self.request.GET.get('phrase')
        qa = self.request.GET.get('qa')
        if q:
            phrase_q &= (Q(title__icontains=q) | Q(title__icontains=q) | Q(title__icontains=q))
        if qa:
            phrase_q &= (Q(author__pk=qa))
        return Post.objects.filter(phrase_q).order_by('-pk')