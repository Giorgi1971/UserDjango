from django.urls import include, path
from .views import *


app_name = 'posts'
urlpatterns = [
    path('', HomeListView.as_view(), name='home'),
    path('posts/', PostListView.as_view(), name='posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post'),
    
    path('example/', ExampleListView.as_view(), name='example'),
    path('example2/', ExampleListView2.as_view(), name='example2'),

    path('follow/<int:pk>/', follow_user, name='follow'),
    path('followw/<int:pk>/', followw_user, name='followw'),
    path('unfollow/<int:kk>/', unfollow, name='unfollow'),
    path('unfollow_user/<int:kk>/', unfollow_user, name='unfollow_user'),
    path('twitter/', FollowListView.as_view(), name='twitter'),
    path('followed/', followed, name='followed'),

    # GRUDE create, update, delete
    path('post/new/', PostCreateView.as_view(), name='create_post'),
    path('post_add/', post_add, name='post_add'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),

    # გამოაქვს 1 - მხოლოდ თავისი პოსტები, 2 - თავისი მონაცემები 
    # path('user_page/', user_page, name='user_page'),
    path('user_page/', UserPage.as_view(), name='user_page'),
    path('user_info/<int:pk>', PersonalDetailView.as_view(), name='user_info'),

    path('u_search/', SearchUserPage.as_view(), name='u_search'),

    # path('categories/', CategoryListView.as_view(), name='categories'),
    # path('category/<int:pk>', CategoryDetailView.as_view(), name='category'),
    # path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),
]