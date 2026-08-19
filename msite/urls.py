from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.index,name='index'),

    path('sign-up/',views.sign,name='sign-up'),

    path('login/',views.login_view,name='login'),

    path('movie_detail/<movie_id>',views.movie_detail,name='movie_detail'),

    path('search/',views.search,name='search-bar'),

    path('movies/',views.more_movies, name='movies'),

    path('actor_movies/<actor_id>',views.actor_movies, name='actor_movies'),

    path('profile-page/',views.profile,name='profile-page'),
    
    path('category_movie/<category_id>',views.category_movie,name='category_movie'),

    path('Tv_Show/<tv_id>',views.Tv,name='tv'),

    path('season/<season_id>',views.season,name='season'),
    
    path('episode/<episode_id>',views.episode,name='episode'),

    path('shows/',views.more_shows, name='shows'),

    path('Favorite',views.watch,name='favorite'),

    path('recommend/',views.recommend,name='recommend'),

    
]
