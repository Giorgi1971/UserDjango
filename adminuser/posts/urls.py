from django.urls import path
from .views import *


app_name = 'posts'
urlpatterns = [
    path('', HomeListView.as_view(), name='home'),
    path('posts/', PostListView.as_view(), name='posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post'),
    
    path('example/', ExampleListView.as_view(), name='example'),
    path('example2/', ExampleListView2.as_view(), name='example2'),

    path('follow/<int:pk>/', follow_user, name='follow'),
    path('followw/<int:pk>/', followw_user, name='followw'),  # ეს მაქვს ფორმის გარეშე follow-ისთვის <a> ტეგით
    path('unfollow/<int:kk>/', unfollow, name='unfollow'),
    path('unfollow_user/<int:kk>/', unfollow_user, name='unfollow_user'), 
    path('twitter/', FollowListView.as_view(), name='twitter'),
    # path('followed/', followed, name='followed'), წასაშლელია წესით
    path('followed/', FollowedListView.as_view(), name='followed'),

    # GRUDE create, update, delete Posts.
    path('post/new/', PostCreateView.as_view(), name='create_post'),  # ამას უსერს ვერ ვაწვდი ჯერ. გასაკეთებელია
    path('post_add/', post_add, name='post_add'),  # თუ კლასით შევქმნი ამას წავშლი
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),

    path('user_page/', UserPageListView.as_view(), name='user_page'),
    path('user_info/<int:pk>', PersonalDetailView.as_view(), name='user_info'),
    # search in users data
    path('u_search/', SearchUserPage.as_view(), name='u_search'),

    path('like/<int:pk>/', like, name='like'),
    path('like/<int:pk>/', like, name='unlike'),  # dasawaeria

    path('messages/', CommentListView.as_view(), name='comment'),
    path('comment_new/', comment_new, name='comment_new'),
    # path('comment_new/', CommentCreateView.as_view(), name='comment_new'),
    # path('comment_add/', comment_add, name='comment_add'),
    path('messages/', CommentListView.as_view(), name='comment'),
]
