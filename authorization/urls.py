from django.urls import paths
from . import view

urlpatterns = [
    path('', views.index, name='index'),
    # path('index/', include('twitterApp.urls')),
    path('twitter_login/', views.twitter_login, name='twitter_login'),
    path('twitter_callback/', views.twitter_callback, name='twitter_callback'),
    path('twitter_logout/', views.twitter_logout, name='twitter_logout'),
]
