#@title Reddit Comment Search with PRAW (Live Data)
import praw
import pandas as pd
from datetime import datetime

# Initialize Reddit client
reddit = praw.Reddit(client_id='zEOZq9FW3kqOSFcuNE4dZg',
                     client_secret='upUOIGxU5o__753cGC9hebhcfxvCxg',
                     user_agent='feedback_scraper:v1.0 (by u/klidoop)',
                     username = 'klidoop',
                     password = '(dseK$V22+=bMg3',
                     check_for_async=False  # Prevent async-related issues
)

# Search latest comments in a subreddit
def search_reddit_comments(subreddit_name, keyword, limit=1000):
    subreddit = reddit.subreddit(subreddit_name)
    comments = []
    for comment in subreddit.comments(limit=limit):
        if keyword.lower() in comment.body.lower():
            comments.append({
                "author": str(comment.author),
                "created_utc": datetime.utcfromtimestamp(comment.created_utc),
                "body": comment.body,
                "permalink": f"https://reddit.com{comment.permalink}"
            })
    return pd.DataFrame(comments)

# Example
df = search_reddit_comments("GooglePixel", "call screen", 500)
print(df.head())
