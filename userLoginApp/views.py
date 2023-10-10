from django.shortcuts import render
from .models import User
import tweepy



# Create your views here.
def home(request):
    user = User.objects
    # for tweet in tweepy.Cursor(api.search_tweets, "Twitter", count=100).items():
        # print(tweet.id)
    return render(request, 'userLoginApp/home.html',{'user':user})

def aboutresearch(request):
    return render(request, 'userLoginApp/aboutresearch.html')