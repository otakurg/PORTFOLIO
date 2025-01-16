from twikit import Client, TooManyRequests
import time
from datetime import datetime
import json
import csv
from configparser import ConfigParser
from random import randint
import asyncio
import tracemalloc
import os
import jwt
from cryptography.fernet import Fernet
import tracemalloc
tracemalloc.start()


# # Load the key
# with open("D:\Storage\Programming\Web-Scraping-projects\secret.key", 'rb') as key_file:
#     key = key_file.read()

# cipher_suite = Fernet(key)

# # Login credentials
# config = ConfigParser()
# config.read('config_enc.ini')
# username = cipher_suite.decrypt(config['X']['username']).decode()
# password = cipher_suite.decrypt(config['X']['password']).decode()
# email = cipher_suite.decrypt(config['X']['email']).decode()

config = ConfigParser()
config.read('config.ini')
username = config['X']['username']
password = config['X']['password']
email = config['X']['email']

# csv file name
current_timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
csv_filename = 'tweets_{current_timestamp}.csv'

# Create csv file
with open(csv_filename, 'w', newline='') as csvfile:
     fieldnames = ['Tweet Count', 'User Name', 'Tweet Text', 'Tweet Created At', 'Retweet Count', 'Favorite Count']
     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
     writer.writeheader()

# Create a client
client = Client(language='en-US')

# Define the file path
cookies_file_path = 'cookies.json'

async def login_client():
        await client.login(auth_info_1=username, auth_info_2=email, password=password)

if not os.path.exists(cookies_file_path):
# Function to login and generate new token
    asyncio.run(login_client())    
    client.save_cookies(cookies_file_path) 
else:
    client.load_cookies(cookies_file_path)

    # # Check if the auth_token is valid or expired
    # token = jwt.decode(client.auth_token, verify=False)['exp']
    # current_time = int(datetime.now().timestamp())
    # if token < current_time:
    #     # Generate a new token
    #     asyncio.run(login_client())
    #     client.save_cookies(cookies_file_path)
    # else:
    #      # Load existing cookies
    #      client.load_cookies(cookies_file_path)
    

# Initialized variables
MINIMUM_TWEETS = 100
MAXIMUM_TWEETS = 20
QUERY = 'Nvidia stock' #input("Enter the query: ")
tweet_data = [] # [tweet_count, tweet.user.name, tweet.text, tweet.created_at, tweet.updated_at, tweet.retweet_count, tweet.favorite_count]

global tweet_count
tweet_count = 0
global tweets
tweets = None

async def get_tweets():
    global tweet_count
    global tweets

    while tweet_count < MINIMUM_TWEETS:
    # Fetch tweets from Twitter API
        if tweets is None:
            print(f"{datetime.now()} - Fetching tweets...")
            try:
                tweets = await client.search_tweet(query=QUERY, product='Top', count=MAXIMUM_TWEETS)
            except TooManyRequests as e:
                rate_limit = datetime.fromtimestamp(e.rate_limit_reset)
                print(f"{datetime.now()} - Rate limit exceeded. Waiting for {rate_limit - datetime.now()} seconds...")
                wait_time = datetime.fromtimestamp(e.rate_limit_reset) - datetime.now()
                time.sleep(wait_time.total_seconds())
                continue
        else:
            wait_time = randint(5, 10); 
            print(f"{datetime.now()} - Fetching next tweets after {wait_time} seconds...")
            time.sleep(wait_time)
            tweets = await tweets.next()
        
        if not tweets:
             print(f"{datetime.now()} - No more tweets found.")
             break

        for tweet in tweets:
            tweet_count += 1
            tweet_data = [str(tweet_count), tweet.user.name, tweet.text, str(tweet.created_at), str(tweet.retweet_count), str(tweet.favorite_count)]

            # Encode each element in tweet_data
            tweet_data_encoded = [element.encode('ascii', 'ignore').decode('ascii') for element in tweet_data]
            #print(tweet_data)
            with open(csv_filename, 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(tweet_data_encoded)
        
        print(f"{datetime.now()} - Fetched {tweet_count} tweets.")
    

asyncio.run(get_tweets())
print(f"{datetime.now()} - Total tweets: {tweet_count}")