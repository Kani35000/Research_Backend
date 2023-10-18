from django.shortcuts import render
from .models import User
import tweepy
from django.contrib import messages
from django.http import HttpResponse
from django.views.generic import View



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
    consumer_key = 'YUJtUmx2TGtWUnJHRGdxUFotOW46MTpjaQ'
    # consumer_secret = 'iOAhAFHK8r84KvjA9MFiFgAeAM8hB3gjJuxnil3dDeMVV1kA4l'
    consumer_secret = '7Bj9_LwAkVFVT66HgzttmBPo2_OZln5svYkCt5ytkkOfO6XLg5'
    access_token = '316095201-BzLPVTiufW84Jidza5cRx8nNgd39Z7I4Fw6VHviK'
    access_token_secret = 'npCvY7nRsqfjPkwUvmMX9FhxR4jYltRkXbcEmISV7kWgU'

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    return tweepy.API(auth)



def twitter_timeline(request):
    api = create_api()
    tweets = api.user_timeline(screen_name='twitter_username', count=10)
    return render(request, 'userLoginApp/home.html', {'tweets': tweets})