from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index/', views.index2, name='index'),
    path('twitter_login/', views.twitter_login, name='twitter_login'),
    path('twitter_callback/', views.twitter_callback, name='twitter_callback'),
    path('twitter_logout/', views.twitter_logout, name='twitter_logout'),
    path('aboutresearch/', views.aboutresearch, name='aboutresearch'),
    path('timeline/', views.timeline, name='timeline'),
    # path('connect_to_endpoint/', views.connect_to_endpoint, name='connect_to_endpoint'),
]
