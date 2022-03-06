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
    return render(request, 'posts/user_page.html')


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
    fields = '__all__'
    model = Post


# ეს არ შლის სურათს მედია ფაილიდან. გადასაწყვეტია ...
class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('posts:posts')