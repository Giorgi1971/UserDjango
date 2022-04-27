from django.contrib.auth import get_user_model
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from .models import *
from django.db.models import Q
from django.urls import reverse_lazy, reverse
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


# Home page, with message by get_context_data()
class HomeListView(ListView):
    queryset = User.objects.all().order_by('?')
    template_name = "posts/home.html"
    context_object_name = 'h_links'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['u_message'] = 'Home'
        return context


class PersonalDetailView(LoginRequiredMixin, DetailView):
    model = get_user_model()
    template_name = 'account/user_detail.html'


class UserPageListView(LoginRequiredMixin, ListView):
    template_name = 'posts/user_page.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)


# Only Post from followed People
class ExampleListView(LoginRequiredMixin, ListView):
    context_object_name = 'list'
    template_name = 'posts/example.html'

    def get_queryset(self):
        qf = Twitter.objects.filter(followed=self.request.user)
        tt = []
        for i in qf:
            p = i.follow.author.all()
            tt.extend(p)
        tk = [i.pk for i in tt]
        query_set = Post.objects.filter(id__in=tk).order_by('?')

        return query_set


# First follow posts, then other. with search and create post
class ExampleListView2(LoginRequiredMixin, ListView):
    model = Post
    context_object_name = 'list'
    template_name = 'posts/example2.html'

    def get_queryset(self):
        #  don't work without [0:num] correctly
        ln = len(Post.objects.all())-1
        p1 = Post.objects.all()[0:ln]
        qf = Twitter.objects.filter(followed=self.request.user)
        tt = []
        for i in qf:
            p = i.follow.author.all()
            tt.extend(p)
        tk = [i.pk for i in tt]
        t = Post.objects.filter(id__in=tk)
        comb = (t | p1).distinct()

        phrase_q = Q()
        q = self.request.GET.get('phrase')
        if q:
            phrase_q &= (Q(title__icontains=q) | Q(text__icontains=q) | Q(title__icontains=q))
        
        query_set = comb.filter(phrase_q)
        return query_set

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qq = self.get_queryset()
        num = qq.count()
        # context['num'] = num
        if 'phrase' in self.request.GET:
            context['message'] = f'Find {num} items'
        return context


# Post detail page.
class PostDetailView(DetailView):
    model = Post
    fields = '__all__'

    # Used for Follow/UnFollow Post owner.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            Twitter.objects.get(follow=self.object.author, followed=self.request.user)
            _foll = False
        except:
            _foll = True
        p1 = Post.objects.get(pk=self.object.pk)
        if p1.like.filter(pk=self.request.user.id).exists():
            liked = False
        else:
            liked = True
        context['liked'] = liked
        context['follow'] = _foll
        context['form_c'] = CommentForm()
        return context


# unfollow someone
def unfollow(request, kk):
    follow = User.objects.get(pk=kk)
    followed = request.user

    f1 = Twitter.objects.filter(follow=follow, followed=followed)
    f1.delete()
    return redirect(reverse("posts:followed"))


# Delete your follower
def unfollow_user(request, kk):
    follow = request.user
    followed = User.objects.get(pk=kk)

    f1 = Twitter.objects.filter(follow=follow, followed=followed)
    f1.delete()
    return redirect(reverse("posts:twitter"))


# List I follow
class FollowedListView(LoginRequiredMixin, ListView):
    login_url = '/user/login/'
    template_name = 'posts/twitter_list.html'

    def get_queryset(self):
        return Twitter.objects.filter(followed=self.request.user)


# User's Who Followed Me
class FollowListView(LoginRequiredMixin, ListView):
    login_url = '/user/login/'
    template_name = 'posts/follow_list.html'

    def get_queryset(self):
        return Twitter.objects.filter(follow=self.request.user)


# Button for Follow someone
@login_required
def follow_user(request, pk):
    post_list = Post.objects.filter(author__pk=pk).order_by()
    if Twitter.objects.filter(follow=pk, followed=request.user.pk):
        message = 'Already follower'
    else:
        follow = User.objects.get(pk=pk)
        follower = request.user
        f1 = Twitter(follow=follow, followed=follower)
        f1.save()
        message = f'You ({follower}) follow {follow}.'
    # return HttpResponseRedirect(reverse('posts:posts')) --- Try to do with this
    return render(request, 'posts/post_list.html', {'page_obj': post_list, 'message': message})


# Maybe this must Delete???? follow without Form, with <a> tag 
def follow_w_user(request, pk):
    message = ''
    post_list = Post.objects.filter(author__pk=pk).order_by()

    return render(request, 'posts/post_list.html', {'page_obj': post_list, 'message': message})


# Search in User's class. Find and follow user.
class SearchUserPage(ListView):
    template_name = 'posts/u_search.html'

    def get_queryset(self):
        phrase_q = Q()
        q = self.request.GET.get('u_search')
        if q:
            phrase_q &= (Q(username__icontains=q) | Q(first_name__icontains=q) | Q(last_name__icontains=q))
        p1 = User.objects.filter(phrase_q)
        return p1.order_by('?')


# all posts list, order by last date. With search and create Post form
class PostListView(ListView):
    model = Post
    paginate_by = 2

    def get_queryset(self):
        phrase_q = Q()
        q = self.request.GET.get('phrase')
        if q:
            phrase_q &= (Q(title__icontains=q) | Q(text__icontains=q) | Q(title__icontains=q))
        print(self.request.user.pk)
        _query = Post.objects.filter(phrase_q) 
        return _query.order_by('-pk')


# create new Post with function
def post_add(request):
    form = PostModelForm()
    form_c = CommentForm()
    if request.method == 'POST':
        if request.user:
            form = PostModelForm(request.POST, request.FILES)
            # print(form)
            if form.is_valid():
                post_m = form.save(commit=False)
                post_m.author = request.user
                # post_m.author = User.objects.get(pk=request.user.pk)
                post_m.save()
                # Good if remember this, maybe used later
                # form.save_m2m()
                return redirect(reverse("posts:posts"))
    return render(request, 'posts/post_form.html', {'form': form, 'form_c': form_c})


# ToDo. Can't pass request user. maybe def save, with request user
class PostCreateView(CreateView):
    model = Post
    form_class = PostModelForm


# Only Post author can get it
class PostUpdateView(UpdateView):
    # fields = ('title', 'text', 'image')
    model = Post
    form_class = PostModelForm


# No delete picture after delete post ...
class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('posts:example2')


def like(request, pk):
    p1 = get_object_or_404(Post, pk=pk)
    p2 = request.user.pk
    if not p1.like.filter(pk=request.user.id).exists():
        p1.like.add(p2)
    else:
        p1.like.remove(p2)
    return HttpResponseRedirect(reverse('posts:post', kwargs={'pk': pk}))


class CommentListView(ListView):
    model = Comment


class CommentCreateView(CreateView):
    model = Comment
    fields = '__all__'
    # template_name = 'posts/post_detail.html'


def comment_new(request):
    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            c1 = form.save(commit=False)
            try:
                request.user.is_authenticated
                c1.writer = request.user
            except:
                return redirect(reverse('account:login'))
            c1.comment_post = Post.objects.get(pk=request.POST.get('post_pk'))
            c1.save()
            return redirect('posts:post', pk=request.POST['post_pk'])
        else:
            return HttpResponse('ERROR, No Valid Form')
    return render(request, 'posts/post_detail.html', {'form': form})
