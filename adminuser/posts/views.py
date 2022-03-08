from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from .models import *
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.urls import reverse_lazy, reverse
from .forms import *
from django.contrib.auth.models import User



def home(request):
    return render(request, 'posts/home.html')


def ddd(request):
    return render(request, 'posts/ddd.html')


@login_required
def user_page(request):
    i = request.user.pk
    print(i)
    print(request.user)
    p = Post.objects.filter(author__pk=i)
    print(p)
    return render(request, 'posts/user_page.html', {'post_list':p})


class PostDetailView(DetailView):
    model = Post


def follow_unique(request):
    message = ''
    follow_pk = request.POST['follow']
    foolowed_pk = request.user.pk
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

def post_add(request):
    form = PostModelForm()
    if request.method == 'POST':
        if request.user.is_staff:
            form = PostModelForm(request.POST, request.FILES)
            print(form)
            if form.is_valid():
                postm = form.save(commit=False)
                print(postm)
                # postm.author = request.user.id
                postm.author = User.objects.get(pk=request.user.pk)
                postm.save()
                # კარგია თუ დამამახსოვრდება, სხვა დროსაც დამჭირდება
                form.save_m2m()
                return redirect(reverse("posts:posts"))
    return render(request, 'posts/post_form.html', {'form':form})


class PostCreateView(CreateView):
    fields = '__all__'
    model = Post


# აქ გვინდა რომ მხოლოდ პოსტის ავტორს შეეძლოს მოხვედრა
class PostUpdateView(UpdateView):
    fields = ('title',)
    model = Post


# ეს არ შლის სურათს მედია ფაილიდან. გადასაწყვეტია ...
class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('posts:posts')