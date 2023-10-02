from django.shortcuts import render
from .models import User
import tweepy

# Your app's API/consumer key and secret can be found under the Consumer Keys
# section of the Keys and Tokens tab of your app, under the
# Twitter Developer Portal Projects & Apps page at
# https://developer.twitter.com/en/portal/projects-and-apps
consumer_key = ""
consumer_secret = ""

# Your account's (the app owner's account's) access token and secret for your
# app can be found under the Authentication Tokens section of the
# Keys and Tokens tab of your app, under the
# Twitter Developer Portal Projects & Apps page at
# https://developer.twitter.com/en/portal/projects-and-apps
access_token = ""
access_token_secret = ""

auth = tweepy.OAuth1UserHandler(
    consumer_key, consumer_secret, access_token, access_token_secret
)

api = tweepy.API(auth)

# If the authentication was successful, this should print the
# screen name / username of the account
print(api.verify_credentials().screen_name)


consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""

auth = tweepy.OAuth1UserHandler(
    consumer_key, consumer_secret, access_token, access_token_secret
)

# Setting wait_on_rate_limit to True when initializing API will initialize an
# instance, called api here, that will automatically wait, using time.sleep,
# for the appropriate amount of time when a rate limit is encountered
api = tweepy.API(auth, wait_on_rate_limit=True)

# This will search for Tweets with the query "Twitter", returning up to the
# maximum of 100 Tweets per request to the Twitter API

# Once the rate limit is reached, it will automatically wait / sleep before
# continuing

for tweet in tweepy.Cursor(api.search_tweets, "Twitter", count=100).items():
    print(tweet.id)

# Create your views here.
def home(request):
    user = User.objects
    for tweet in tweepy.Cursor(api.search_tweets, "Twitter", count=100).items():
        print(tweet.id)
    return render(request, 'userLoginApp/home.html',{'user':user})