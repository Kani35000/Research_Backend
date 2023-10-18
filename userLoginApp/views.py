# from django.shortcuts import render
# from .models import User
# import tweepy
# from django.contrib import messages
# from django.http import HttpResponse
# from django.views.generic import View
# import datetime

# import os
# from requests_oauthlib import OAuth1Session

# from django.apps import AppConfig

# from django.contrib.auth import login, logout
# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render, redirect
# from .decorators import twitter_login_required
# from .models import TwitterAuthToken, TwitterUser
# from .authorization import create_update_user_from_twitter, check_token_still_valid
# from twitter_api.twitter_api import TwitterAPI

# # Create your views here.

# def home(request):
#     # user = User.objects
#     # for tweet in tweepy.Cursor(api.search_tweets, "Twitter", count=100).items():
 
#     return render(request, 'userLoginApp/home.html')

# def submitform(request):
#     messages.info(request, "Not Available at this moment!")
#     return render(request, 'userLoginApp/home.html')


# def aboutresearch(request):
#     return render(request, 'userLoginApp/aboutresearch.html')






# # Create your views here.
# def twitter_login(request):
#     twitter_api = TwitterAPI()
#     url, oauth_token, oauth_token_secret = twitter_api.twitter_login()
#     if url is None or url == '':
#         messages.add_message(request, messages.ERROR, 'Unable to login. Please try again.')
#         return render(request, 'authorization/error_page.html')
#     else:
#         twitter_auth_token = TwitterAuthToken.objects.filter(oauth_token=oauth_token).first()
#         if twitter_auth_token is None:
#             twitter_auth_token = TwitterAuthToken(oauth_token=oauth_token, oauth_token_secret=oauth_token_secret)
#             twitter_auth_token.save()
#         else:
#             twitter_auth_token.oauth_token_secret = oauth_token_secret
#             twitter_auth_token.save()
#         return redirect(url)


# def twitter_callback(request):
   
#     if 'denied' in request.GET:
#         messages.add_message(request, messages.ERROR, 'Unable to login or login canceled. Please try again.')
#         return render(request, 'authorization/error_page.html')
#     twitter_api = TwitterAPI()
#     oauth_verifier = request.GET.get('oauth_verifier')
#     oauth_token = request.GET.get('oauth_token')
#     twitter_auth_token = TwitterAuthToken.objects.filter(oauth_token=oauth_token).first()
#     if twitter_auth_token is not None:
#         access_token, access_token_secret = twitter_api.twitter_callback(oauth_verifier, oauth_token, twitter_auth_token.oauth_token_secret)
#         if access_token is not None and access_token_secret is not None:
#             twitter_auth_token.oauth_token = access_token
#             twitter_auth_token.oauth_token_secret = access_token_secret
#             twitter_auth_token.save()
#             # Create user
#             info = twitter_api.get_me(access_token, access_token_secret)
#             if info is not None:
#                 twitter_user_new = TwitterUser(twitter_id=info[0]['id'], screen_name=info[0]['username'],
#                                                name=info[0]['name'], profile_image_url=info[0]['profile_image_url'])
#                 twitter_user_new.twitter_oauth_token = twitter_auth_token
#                 user, twitter_user = create_update_user_from_twitter(twitter_user_new)
#                 print(user, "************************")
#                 if user is not None:
#                     login(request, user)
#                     name= info[0]["name"]
#                     id = user.args
#                     return redirect('index')
                    
#                     # return render(request, 'userLoginApp/home.html', {"user": user} , name, id)
#             else:
#                 messages.add_message(request, messages.ERROR, 'Unable to get profile details. Please try again.')
#                 return render(request, 'authorization/error_page.html')
#         else:
#             messages.add_message(request, messages.ERROR, 'Unable to get access token. Please try again.')
#             return render(request, 'authorization/error_page.html')
#     else:
#         messages.add_message(request, messages.ERROR, 'Unable to retrieve access token. Please try again.')
#         return render(request, 'authorization/error_page.html')


# @login_required
# @twitter_login_required
# def index(request):
#     api = tweepy.API(auth)
#     auth = tweepy.OAuthHandler(consumer_key= 'hNW5KMJGjcFnhlu5ZKgbmS64V', consumer_secret= 'NP7YaHbsttCGJtCR1LkelRlAaHuGBhhKb19QvkvCaoSL5wuoW1', callback_url= 'https://researchnortheastern-f0da7b5714f0.herokuapp.com/')
#     session.set('request_token', auth.request_token['oauth_token'])
#     for tweet in tweepy.Cursor(api.search_tweets, q='tweepy').items(10):        
#         print(tweet.text)
#     return render(request, 'userLoginApp/home.html')


# @login_required
# def twitter_logout(request):
#     logout(request)
#     return redirect('index')




# def tweepytweet(request):
#     # api = tweepy.API(auth)
    
#     # auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback_url)
#     consumer_key = 'hNW5KMJGjcFnhlu5ZKgbmS64V'
#     consumer_secret = 'NP7YaHbsttCGJtCR1LkelRlAaHuGBhhKb19QvkvCaoSL5wuoW1'
#     access_token = '316095201-JN50wcjT5SpZi2zBAjozXJSNLDvarkjIWtKaFh3B'
#     access_token_secret = 'mMOzbxi12MrF8NSD2I5Nv4sgGGBSjWJStdKpTdzKPi24D'

#     client = tweepy.Client(
#     consumer_key=consumer_key,
#     consumer_secret=consumer_secret,
#     access_token=access_token,
#     access_token_secret=access_token_secret
#     )
    
  
   

#     auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
#     auth.set_access_token(access_token, access_token_secret)
#     api = tweepy.API(auth)

    
    
#     api = tweepy.API(auth)
#     # session.set('request_token', auth.request_token['oauth_token'])
#     for tweet in tweepy.Cursor(api.search_tweets, q='tweepy').items(10):
#        print(tweet.text)
#     return redirect('home')























