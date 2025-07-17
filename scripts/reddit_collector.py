import praw
import json
import os
import requests
import time
from datetime import datetime
from dotenv import load_dotenv

# Carica le variabili d'ambiente dal file .env
load_dotenv() 

# URL dell'input HTTP di Logstash per i dati di Reddit
LOGSTASH_URL = 'http://localhost:8082'

# Reddit API credentials
reddit = praw.Reddit(
    client_id=os.getenv('REDDIT_CLIENT_ID'),
    client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
    user_agent='market_intelligence_bot/1.0'
)

# Financial subreddits
subreddits = ['stocks', 'investing', 'SecurityAnalysis', 'ValueInvesting', 
              'wallstreetbets', 'StockMarket', 'pennystocks']

def collect_reddit_posts():
    """Raccoglie i post 'hot' dai subreddit finanziari specificati."""
    results = []
    
    for subreddit_name in subreddits:
        try:
            subreddit = reddit.subreddit(subreddit_name)
            
            for submission in subreddit.hot(limit=50):
                post_data = {
                    'id': submission.id,
                    'title': submission.title,
                    'selftext': submission.selftext,
                    'score': submission.score,
                    'upvote_ratio': submission.upvote_ratio,
                    'num_comments': submission.num_comments,
                    'created_utc': submission.created_utc,
                    'author': str(submission.author),
                    'subreddit': subreddit_name,
                    'url': submission.url
                }
                results.append(post_data)
                
        except Exception as e:
            print(f"Error collecting from r/{subreddit_name}: {e}")
    
    return results

def send_to_logstash(data):
    """Invia un singolo record a Logstash tramite una richiesta POST."""
    try:
        response = requests.post(LOGSTASH_URL, json=data, timeout=5)
        response.raise_for_status() # Lancia un errore per status HTTP 4xx/5xx
        print(f"Successfully sent post {data['id']} to Logstash.")
    except requests.exceptions.RequestException as e:
        print(f"Error sending to Logstash: {e}")

if __name__ == "__main__":
    print("Starting Reddit collector...")
    posts = collect_reddit_posts()
    print(f"Collected {len(posts)} posts. Sending to Logstash...")
    
    for post in posts:
        send_to_logstash(post)
        time.sleep(0.1) # Piccola pausa per non sovraccaricare Logstash
        
    print("Reddit collection finished.")