from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_list_or_404, render, redirect
from django.views import View
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from .models import *
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.urls import reverse_lazy, reverse
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin


class HomeListView(ListView):
    queryset = User.objects.all().order_by('?')[0:5]
    template_name = 'posts/home.html'
    context_object_name = 'hlinks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['u_message'] = ''
        return context


class PersonalDetailView(DetailView):
    model = get_user_model()
    template_name = 'account/user_detail.html'


# საკუთარი პოსტების გამოტანა user_page.html 
@login_required
def user_page(request):
    post_list = Post.objects.filter(author=request.user)
    return render(request, 'posts/user_page.html', {'post_list':post_list})


class UserPage(LoginRequiredMixin, ListView):
    template_name = 'posts/user_page.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)


class ExampleListView(LoginRequiredMixin, ListView):
    context_object_name = 'list'
    template_name = 'posts/example.html'
    def get_queryset(self):
        qf = Twitter.objects.filter(followed=self.request.user) # .annotate(tt=(follow__post_set=))
        tt = []
        for i in qf:
            print(i.follow.author.all())
            # p = i.follow.post_set.all()
            p = i.follow.author.all()
            tt.extend(p)
        tk = [i.pk for i in tt]
        querset = Post.objects.filter(id__in=tk).order_by('?')

        return querset


class ExampleListView2(LoginRequiredMixin, ListView):
    context_object_name = 'list'
    template_name = 'posts/example2.html'

    def get_queryset(self):
        qf = Twitter.objects.filter(followed=self.request.user) # .annotate(tt=(follow__post_set=))
        return qf


# ცალკეული პოსტის ნახვა, თუ ავტორი ნახულობს აქვს რედაქტირების საშუალება
class PostDetailView(DetailView):
    model = Post
    # შეგვიძლია გავატანოთ დამატებით რაც გვინდა, მაგარია
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            Twitter.objects.get(follow=self.object.author, followed=self.request.user)
            dd = False
        except:
            dd = True
        context['follow'] = dd
        return context


def unfollow(request, kk):
    follow = User.objects.get(pk=kk)
    followed = request.user

    f1 = Twitter.objects.filter(follow=follow, followed=followed)
    f1.delete()
    return redirect(reverse("posts:followed"))


def unfollow_user(request, kk):
    follow = request.user
    followed = User.objects.get(pk=kk)

    f1 = Twitter.objects.filter(follow=follow, followed=followed)
    f1.delete()
    return redirect(reverse("posts:twitter"))


@login_required
def followed(request):
    f1 = Twitter.objects.filter(followed=request.user)
    return render(request, 'posts/twitter_list.html', {'twitter_list':f1})


class FollowListView(LoginRequiredMixin, ListView):
    login_url = '/user/login/'
    template_name = 'posts/follow_list.html'

    def get_queryset(self):
        return Twitter.objects.filter(follow=self.request.user)


def follow_user(request, pk):
    message = ''
    # follow_pk = request.POST['follow']
    post_list = Post.objects.filter(author__pk=pk).order_by()
    print(post_list)
    if Twitter.objects.filter(follow=pk, followed=request.user.pk):
        message = 'Already follower'
    else:
        follow = User.objects.get(pk=pk)
        follower = request.user
        f1 = Twitter(follow=follow, followed=follower)
        f1.save()
        message = f'follow {follow} follower'
    # return HttpResponseRedirect(reverse('posts:posts'))    
    return render(request, 'posts/post_list.html', {'page_obj':post_list, 'message':message})


def followw_user(request, pk):
    message = ''
    post_list = Post.objects.filter(author__pk=pk).order_by()

    return render(request, 'posts/post_list.html', {'page_obj':post_list, 'message':message})


class SearchUserPage(ListView):
    template_name = 'posts/u_search.html'

    def get_queryset(self):
        phrase_q = Q()
        q = self.request.GET.get('u_search')
        print(q)
        if q:
            phrase_q &= (Q(username__icontains=q) | Q(last_name__icontains=q) | Q(username__icontains=q))
        print(self.request.user.pk)
        p1 = User.objects.filter(phrase_q) #.filter(author__followed__pk=self.request.user.pk)
        return p1.order_by('-pk')


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

# create new Post with function
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
    model = Post
    form_class = PostModelForm

    # if form_class.is_valid():
    #     form_class.save(author=request.user, commit=False)

    # fields = '__all__'

    # def post(self):
    #     form_class.author = 


# აქ გვინდა რომ მხოლოდ პოსტის ავტორს შეეძლოს მოხვედრა
class PostUpdateView(UpdateView):
    fields = ('title', 'text', 'image')
    model = Post


# ეს არ შლის სურათს მედია ფაილიდან. გადასაწყვეტია ...
class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('posts:posts')
