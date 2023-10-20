import tweepy 
import json
import sys
import pandas as pd
import requests


# def timeline(requests):
    

# Define the API endpoint URL
url = "https://api.twitter.com/2/tweets"

    # Make a GET request to the API
# response = requests.get(url)
# tweets = response.json()
# print(tweets)

    # Check if the request was successful (status code 200 indicates success)
    # if response.status_code == 200:
    #     # Parse the JSON response
    #     tweets = response.json()

    #     # Now 'data' contains the JSON data from the API
    #     print(tweets)
    # else:
    #     # Handle the error if the request was not successful
    #     print(f"Request failed with status code: {response.status_code}")

        
    # with open('tweets.json') as json_file:
    #         data_list = json.load(json_file)

    #     tweet_data_frame = pd.DataFrame.from_dict(data_list)
    #     print(tweet_data_frame)
    #     print(data_list)
    #     return render(request, 'authorization/timeline.html')    