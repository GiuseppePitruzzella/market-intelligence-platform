import tweepy
import json
import os
import requests
import time
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# --- CONFIGURATION ---
LOGSTASH_URL = 'http://localhost:8081'
# Run the collection every 15 minutes (15 * 60 seconds)
SLEEP_INTERVAL_SECONDS = 900 
# Twitter API credentials
bearer_token = os.getenv('TWITTER_BEARER_TOKEN')

# --- INITIALIZE API CLIENT ---
client = tweepy.Client(bearer_token=bearer_token)

# Financial keywords to search
keywords = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 
           'stock market', 'investing', 'trading', 'finance']

def collect_tweets():
    """Cerca tweet recenti costruendo un'unica query per essere più efficiente."""
    
    formatted_keywords = [f'"{k}"' if ' ' in k else k for k in keywords]
    query = f"({' OR '.join(formatted_keywords)}) -is:retweet lang:en"
    
    print(f"Executing query: {query}")
    
    try:
        tweets = client.search_recent_tweets(
            query=query,
            max_results=100, # Request up to 100 tweets per run
            tweet_fields=['created_at', 'author_id', 'public_metrics', 'context_annotations']
        )
        
        results = []
        if tweets.data:
            for tweet in tweets.data:
                matched_keyword = next((kw for kw in keywords if kw.lower() in tweet.text.lower()), "unknown")
                tweet_data = {
                    'id': tweet.id,
                    'text': tweet.text,
                    'created_at': tweet.created_at.isoformat(),
                    'author_id': tweet.author_id,
                    'retweet_count': tweet.public_metrics['retweet_count'],
                    'like_count': tweet.public_metrics['like_count'],
                    'reply_count': tweet.public_metrics['reply_count'],
                    'quote_count': tweet.public_metrics['quote_count'],
                    'keyword': matched_keyword
                }
                results.append(tweet_data)
        return results
            
    except Exception as e:
        print(f"Error collecting tweets: {e}")
        return []

def send_to_logstash(data):
    """Invia un singolo record a Logstash tramite una richiesta POST."""
    try:
        response = requests.post(LOGSTASH_URL, json=data, timeout=5)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error sending tweet {data.get('id')} to Logstash: {e}")

if __name__ == "__main__":
    print("--- Starting Twitter Collector Service ---")
    while True:
        print(f"[{datetime.now()}] Running scheduled collection...")
        tweets = collect_tweets()
    
        if tweets:
            print(f"Collected {len(tweets)} tweets. Sending to Logstash...")
            for tweet in tweets:
                send_to_logstash(tweet)
                time.sleep(0.05) # Small delay between posts to Logstash
        else:
            print("No new tweets collected in this run.")
        
        print(f"Collection finished. Sleeping for {SLEEP_INTERVAL_SECONDS / 60} minutes...")
        time.sleep(SLEEP_INTERVAL_SECONDS)