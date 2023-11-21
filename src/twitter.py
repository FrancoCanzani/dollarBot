import tweepy
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()


class Twitter:
    def __init__(self):
        # Initialize the Tweepy client inside the class constructor
        self.client = tweepy.Client(
            consumer_key=os.getenv("consumer_key"),
            consumer_secret=os.getenv("consumer_secret"),
            access_token=os.getenv("access_token"),
            access_token_secret=os.getenv("access_token_secret"),
        )

    def create_tweet(self, text):
        # Create a tweet using the Tweepy client
        try:
            self.client.create_tweet(text=text)
            print("Tweet created successfully")
        except Exception as e:
            print(f"An error occurred: {e}")
