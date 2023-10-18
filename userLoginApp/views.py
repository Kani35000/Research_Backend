from django.shortcuts import render
from .models import User
import tweepy
from django.contrib import messages
from django.http import HttpResponse
from django.views.generic import View

import json
import os
from requests_oauthlib import OAuth1Session

from django.apps import AppConfig

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .decorators import twitter_login_required
from .models import TwitterAuthToken, TwitterUser
from .authorization import create_update_user_from_twitter, check_token_still_valid
from twitter_api.twitter_api import TwitterAPI

# Create your views here.

def home(request):
    # user = User.objects
    # for tweet in tweepy.Cursor(api.search_tweets, "Twitter", count=100).items():
    
    return render(request, 'userLoginApp/home.html')

def submitform(request):
    messages.info(request, "Not Available at this moment!")
    return render(request, 'userLoginApp/home.html')


def aboutresearch(request):
    return render(request, 'userLoginApp/aboutresearch.html')






# Create your views here.
def twitter_login(request):
    twitter_api = TwitterAPI()
    url, oauth_token, oauth_token_secret = twitter_api.twitter_login()
    if url is None or url == '':
        messages.add_message(request, messages.ERROR, 'Unable to login. Please try again.')
        return render(request, 'authorization/error_page.html')
    else:
        twitter_auth_token = TwitterAuthToken.objects.filter(oauth_token=oauth_token).first()
        if twitter_auth_token is None:
            twitter_auth_token = TwitterAuthToken(oauth_token=oauth_token, oauth_token_secret=oauth_token_secret)
            twitter_auth_token.save()
        else:
            twitter_auth_token.oauth_token_secret = oauth_token_secret
            twitter_auth_token.save()
        return redirect(url)


def twitter_callback(request):
   
    if 'denied' in request.GET:
        messages.add_message(request, messages.ERROR, 'Unable to login or login canceled. Please try again.')
        return render(request, 'authorization/error_page.html')
    twitter_api = TwitterAPI()
    oauth_verifier = request.GET.get('oauth_verifier')
    oauth_token = request.GET.get('oauth_token')
    twitter_auth_token = TwitterAuthToken.objects.filter(oauth_token=oauth_token).first()
    if twitter_auth_token is not None:
        access_token, access_token_secret = twitter_api.twitter_callback(oauth_verifier, oauth_token, twitter_auth_token.oauth_token_secret)
        if access_token is not None and access_token_secret is not None:
            twitter_auth_token.oauth_token = access_token
            twitter_auth_token.oauth_token_secret = access_token_secret
            twitter_auth_token.save()
            # Create user
            info = twitter_api.get_me(access_token, access_token_secret)
            if info is not None:
                twitter_user_new = TwitterUser(twitter_id=info[0]['id'], screen_name=info[0]['username'],
                                               name=info[0]['name'], profile_image_url=info[0]['profile_image_url'])
                twitter_user_new.twitter_oauth_token = twitter_auth_token
                user, twitter_user = create_update_user_from_twitter(twitter_user_new)
                print(user, "************************")
                if user is not None:
                    login(request, user)
                    name= info[0]["name"]
                    id = user.args
                    # return redirect('index')
                    return render(request, 'userLoginApp/home.html', {"user": user} , name, id)
            else:
                messages.add_message(request, messages.ERROR, 'Unable to get profile details. Please try again.')
                return render(request, 'authorization/error_page.html')
        else:
            messages.add_message(request, messages.ERROR, 'Unable to get access token. Please try again.')
            return render(request, 'authorization/error_page.html')
    else:
        messages.add_message(request, messages.ERROR, 'Unable to retrieve access token. Please try again.')
        return render(request, 'authorization/error_page.html')


@login_required
@twitter_login_required
def index(request):
    print(request.user)
    if request.user:
        id = request.user.id
        username= requst.user.username
        is_authenticated= requst.user.is_authenticated
        is_active= requst.user.is_active
        date_joined= requst.user.date_joined        
        return render(request, 'userLoginApp/home.html', id, date_joined, is_active, is_authenticated, username)

    


@login_required
def twitter_logout(request):
    logout(request)
    return redirect('index')


# def home(request):
#     logout(request)
#     return render(request, 'home.html')



def create_api():
    # Replace with your Twitter API keys
    # consumer_key = 'sVgstwrdGQm2PQXSir9KaOkYP'
    consumer_key = 'mh00Pas3yHx4BO0CcEUuIXIij'
    # consumer_secret = 'iOAhAFHK8r84KvjA9MFiFgAeAM8hB3gjJuxnil3dDeMVV1kA4l'
    consumer_secret = 'KPmSQFaopcsZD5FqFDXr129tIEdJlfb7hw82Dry8aCnhd3i2kR'
    access_token = '316095201-JN50wcjT5SpZi2zBAjozXJSNLDvarkjIWtKaFh3B'
    access_token_secret = 'mMOzbxi12MrF8NSD2I5Nv4sgGGBSjWJStdKpTdzKPi24D'
    # auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    # auth.set_access_token(access_token, access_token_secret)

    return tweepy.API(auth)



def twitter_timeline(request):
    api = create_api()
    tweets = api.user_timeline(screen_name='twitter_username', count=10)
    return render(request, 'userLoginApp/home.html', {'tweets': tweets})


consumer_key = 'mh00Pas3yHx4BO0CcEUuIXIij'
# consumer_secret = 'iOAhAFHK8r84KvjA9MFiFgAeAM8hB3gjJuxnil3dDeMVV1kA4l'
consumer_secret = 'KPmSQFaopcsZD5FqFDXr129tIEdJlfb7hw82Dry8aCnhd3i2kR'
access_token = '316095201-JN50wcjT5SpZi2zBAjozXJSNLDvarkjIWtKaFh3B'

access_token_secret = 'mMOzbxi12MrF8NSD2I5Nv4sgGGBSjWJStdKpTdzKPi24D'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

auth = tweepy.OAuth1UserHandler(
    consumer_key, consumer_secret,
    access_token, access_token_secret
)
































# last try starts here


# File to save credentials
CREDENTIALS_FILE = "twitter_credentials.json"

def authenticate(request):
    consumer_key = 'mh00Pas3yHx4BO0CcEUuIXIij'
    # consumer_key = os.environ.get("CONSUMER_KEY")
    consumer_secret = "KPmSQFaopcsZD5FqFDXr129tIEdJlfb7hw82Dry8aCnhd3i2kR"
    # consumer_secret = os.environ.get("CONSUMER_SECRET")
    if consumer_key is None or consumer_secret is None:
        print("Consumer key or consumer secret is missing.")

    # Check if credentials file exists
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, 'r') as file:
            creds = json.load(file)
            return creds["consumer_key"], creds["consumer_secret"], creds["access_token"], creds["access_token_secret"]

    # If credentials file doesn't exist, proceed with authentication
    # Get request token
    request_token_url = "https://api.twitter.com/oauth/request_token?oauth_callback=oob&x_auth_access_type=write"
    oauth = OAuth1Session(consumer_key, client_secret=consumer_secret)
    fetch_response = oauth.fetch_request_token(request_token_url)

    resource_owner_key = fetch_response.get("oauth_token")
    resource_owner_secret = fetch_response.get("oauth_token_secret")

    # Get authorization
    base_authorization_url = "https://api.twitter.com/oauth/authorize"
    authorization_url = oauth.authorization_url(base_authorization_url)
    
    print("Please go here and authorize:", authorization_url)
    verifier = input("Paste the PIN here: ")

    # Get the access token
    access_token_url = "https://api.twitter.com/oauth/access_token"
    oauth = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=resource_owner_key,
        resource_owner_secret=resource_owner_secret,
        verifier=verifier,
    )
    oauth_tokens = oauth.fetch_access_token(access_token_url)

    access_token = oauth_tokens["oauth_token"]
    access_token_secret = oauth_tokens["oauth_token_secret"]

    # Save the credentials to a file
    with open(CREDENTIALS_FILE, 'w') as file:
        json.dump({
            "consumer_key": consumer_key,
            "consumer_secret": consumer_secret,
            "access_token": access_token,
            "access_token_secret": access_token_secret
        }, file)

    return consumer_key, consumer_secret, access_token, access_token_secret

if __name__ == '__main__':
    authenticate()
    
     
