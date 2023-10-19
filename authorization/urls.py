from django.urls import path
from authorization import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('twitter_login/', views.twitter_login, name='twitter_login'),
    path('twitter_callback/', views.twitter_callback, name='twitter_callback'),
    path('twitter_logout/', views.twitter_logout, name='twitter_logout'),
]