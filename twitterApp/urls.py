"""twitterApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

# import userLoginApp.views
# from userLoginApp import views


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', views.home),
    # path('submitform', views.submitform),
    # path('aboutresearch/', views.aboutresearch, name='aboutresearch'),
    
    # path('tweepytweet/', views.tweepytweet, name='tweepytweet'),

    # path('twitter_login/', views.twitter_login, name='twitter_login'),
    # path('twitter_callback/', views.twitter_callback, name='twitter_callback'),
    # path('twitter_logout/', views.twitter_logout, name='twitter_logout'),
    
    path('authorization/', include('authorization.urls')),
    # path('', views.index),
    # path('twitter_login/', views.twitter_login, name='twitter_login'),
    # path('twitter_callback/', views.twitter_callback, name='twitter_callback'),
    # path('twitter_logout/', views.twitter_logout, name='twitter_logout'),
]
# from django.urls import path
# from . import views
