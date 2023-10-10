from django.shortcuts import render
from .models import User
import tweepy
from django.contrib import messages
from django.http import HttpResponse
from django.views.generic import View

# Create your views here.

def home(request):
    user = User.objects
    # for tweet in tweepy.Cursor(api.search_tweets, "Twitter", count=100).items():
            # print(tweet.id)
    return render(request, 'userLoginApp/home.html',{'user':user})

def submitform(request):
    messages.info(request, "Not Available at this moment!")
    return render(request, 'userLoginApp/home.html')


def aboutresearch(request):
    return render(request, 'userLoginApp/aboutresearch.html')


# messages.info(request, "Not Available at this moment!")
    # return render(request, 'home.html',{'user':user})

# if form.is_valid():
#         for fs in formsets:
#             if fs.is_valid():
#                 # Messages test start
#                 messages.success(request, "Profile updated successfully!")
#                 # Messages test end
#                 fs.save()
#             else:
#                 messages.error(request, "It didn't save!")