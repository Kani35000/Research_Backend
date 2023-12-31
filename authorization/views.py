from django.shortcuts import render
import json
import pandas as pd
# from django.http import HttpResponse
from django.http import JsonResponse
import tweepy

import requests

#importing classifier
from .app import predict

from create_csv import create_csv



from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .decorators import twitter_login_required
from .models import TwitterAuthToken, TwitterUser
from .authorization import create_update_user_from_twitter, check_token_still_valid
from twitter_api.twitter_api import TwitterAPI
from .tweets import create_url, get_params, connect_to_endpoint

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
    
    # Create a Tweepy API object
    
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
                    # #calling the tweets
                    # url = create_url(user.id)
                    # params = get_params()
                    # json_response = connect_to_endpoint(url, params)
                    # response_in_json = json.dumps(json_response, indent=4, sort_keys=True)
                    # if this is a POST request we need to process the form data
                    if request.method == "POST":
                        # create a form instance and populate it with data from the request:
                        tweets = request.POST.get('tweets')
                        # reminder: recheck after deploying
                        create_csv(tweets)
                        result = predict('tweet.csv')
                        result.to_csv('predictions.csv', index=False) 
                        file_path = 'predictions.csv'
                        df = pd.read_csv(file_path)
                        if df.loc[row_index, 'predictions'] == 1:
                            text = "This is News"
                            console.log(text)
                            return render(request, 'authorization/home.html', {'user': user}, {'text', text})

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


TWITTER_API_KEY = '5bhCPf1JSdAH272oBX3HbRK3F'
TWITTER_API_SECRET = 'UTNRXOsyKwyC2lBC4GJzoLgIkPvH5AcGmbK3SaerptwdEQtdiu'
TWITTER_ACCESS_TOKEN = '316095201-6coCa0IMbTtJMrTusBKvgZLlgaHw3pjG54WWK0C4'
TWITTER_ACCESS_TOKEN_SECRET = 'Vi01ttZk6vINYlQ216yomi4mmH50tjg9S4xjaF0MFp8yQ'

def get_tweets(request, username, count=10):
    auth = tweepy.OAuthHandler(TWITTER_API_KEY,TWITTER_API_SECRET)
    auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    try:
        tweets = api.user_timeline(screen_name=username, count=count)
        tweet_data = [{'text': tweet.text, 'created_at': tweet.created_at} for tweet in tweets]
        return JsonResponse({'tweets': tweet_data})
    except Exception as e:
        return JsonResponse({'error': str(e)})



@login_required
@twitter_login_required
def index(request):
    return render(request, 'authorization/home.html')


@login_required
def twitter_logout(request):
    # delete(TwitterUser.objects.get(id=pk))
    logout(request)
    return redirect('index')



@login_required
@twitter_login_required
def index2(request):
    return render(request, 'authorization/home.html')



@login_required
@twitter_login_required
def timeline_in_json(request):
    # Authentication: Retrieve user-specific tokens here.
    
    # oauth_token = request.GET.get('oauth_token')

    # Define the Twitter API endpoint
    api_url = "https://api.twitter.com/2/tweets"

    # Set up headers with the user's access token
    # headers = {
    #     "Authorization": f"Bearer {oauth_token}"
    # }

    # Make the API request
    response = requests.get(api_url)
    twitter_data = response.json()
    return render(request, 'authorization/timeline.html', {'twitter_data': twitter_data})


# def timeline_in_table(request):
#     url = "https://api.twitter.com/2/tweets"
#     # response = requests.get(url)
#     tweets = timeline_in_json(request)
#     print(tweets)

#     with open('tweets') as json_file:
#         data_list = json.load(json_file)

#         tweet_data_frame = pd.DataFrame.from_dict(data_list)
#         print(tweet_data_frame)
#         print(data_list)
#         return render(request, 'authorization/timeline.html', {'tweet_data_frame': tweet_data_frame})   

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






