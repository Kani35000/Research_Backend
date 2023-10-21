from django.shortcuts import render
import json
import pandas as pd

# Create your views here.
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .decorators import twitter_login_required
from .models import TwitterAuthToken, TwitterUser
from .authorization import create_update_user_from_twitter, check_token_still_valid
from twitter_api.twitter_api import TwitterAPI


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
                if user is not None:
                    login(request, user)
                    print(user)
                    # tweets = api.user_timeline(screen_name= user.username, count=10)
                    # return redirect('index2')
                    return render(request, 'authorization/home.html', {'user': user})
                    
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
    return render(request, 'authorization/home.html')


@login_required
def twitter_logout(request):
    logout(request)
    return redirect('index')



@login_required
@twitter_login_required
def index2(request):
    return render(request, 'authorization/home.html')


def timeline(requests):
    url = "https://api.twitter.com/2/tweets"
    response = requests.get(url)
    tweets = response.json()
    print(tweets)

    with open('tweets.json') as json_file:
        data_list = json.load(json_file)

        tweet_data_frame = pd.DataFrame.from_dict(data_list)
        print(tweet_data_frame)
        print(data_list)
        return render(request, 'authorization/timeline.html', {'tweet_data_frame': tweet_data_frame})   

# params = {
#     "start_time": "2023-01-01T00:00:00Z",
#     "end_time": "2023-01-31T23:59:59Z",
#     # Other parameters like 'query' can be added if needed.
# }

# def timeline(request):
#     import requests

#     # Define the API endpoint URL
#     url = "https://api.example.com/data"

#     # Make a GET request to the API
#     response = requests.get(url)

#     # Check if the request was successful (status code 200 indicates success)
#     if response.status_code == 200:
#         # Parse the JSON response
#         data = response.json()

#         # Now 'data' contains the JSON data from the API
#         print(data)
#     else:
#         # Handle the error if the request was not successful
#         print(f"Request failed with status code: {response.status_code}")

        
#     with open('tweets.json') as json_file:
#             data_list = json.load(json_file)

#         tweet_data_frame = pd.DataFrame.from_dict(data_list)
#         print(tweet_data_frame)
#         print(data_list)
#         return render(request, 'authorization/timeline.html')    


def aboutresearch(request):
    return render(request, 'authorization/aboutresearch.html')






