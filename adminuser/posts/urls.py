from django.urls import include, path
from .views import *


app_name = 'posts'
urlpatterns = [
    path('', home, name='home'),
    path('posts/', PostListView.as_view(), name='posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post'),
    
    path('example/', ExampleListView.as_view(), name='example'),

    path('follow/', follow_unique, name='follow'),
    path('following/<int:kk>/', following, name='following'),
    path('twitter/', FollowListView.as_view(), name='twitter'),
    path('followed/', followed, name='followed'),


    path('post/new/', PostCreateView.as_view(), name='create_post'),

    path('post_add/', post_add, name='post_add'),

    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),

    path('user_page/', user_page, name='user_page'),
    path('user_info/<int:pk>', PersonalDetailView.as_view(), name='user_info'),

    path('ddd/', ddd, name='ddd'),

    # path('categories/', CategoryListView.as_view(), name='categories'),
    # path('category/<int:pk>', CategoryDetailView.as_view(), name='category'),
    # path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),
]