from django.urls import path
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings

app_name = 'music_app'

from . import views
urlpatterns = [
    path('',views.music_home, name='music_home'),
    path('musician/<int:musician_id>', views.musician_page, name='musician_page'),
    path('like/<int:post_id>', views.like, name='like'),
    path('comment/<int:post_id>', views.post_comment, name='post_comment'),
    path('post/<int:musician_id>', views.post_post, name='post_post'),
    path('add_musician', views.add_musician, name='add_musician'),
    path('genre_home/<int:genre_id>', views.genrebased_home, name='genrebased_home' ),
    path('follow/<int:musician_id>', views.follow_musician, name='follow_musician'), 
    path('sign_in', views.sign_in, name='sign_in'), 
    path('sign_up', views.sign_up, name='sign_up'),
    path('search',views.search, name='search'),
    path('logout', views.logout_view, name='logout'),
    path('send_to_signin', views.send_to_signin, name='send_to_signin'),
] 

