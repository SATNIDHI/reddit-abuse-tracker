# scripts/data_collection/collect_sample_data.py
"""
Quick script to collect sample Reddit data
"""
import sys
import os
import json
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from data_collection.reddit_client import RedditClient

def collect_sample_data():
    """Collect sample data from Reddit"""
    client = RedditClient()
    
    # Collect posts from different subreddits
    subreddits = ['Python', 'programming', 'technology', 'AskReddit']
    all_posts = []
    
    for subreddit in subreddits:
        print(f"📊 Collecting from r/{subreddit}...")
        posts = client.get_subreddit_posts(subreddit, limit=10)
        all_posts.extend(posts)
    
    # Save to JSON file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"data/sample/sample_posts_{timestamp}.json"
    
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    with open(filename, 'w') as f:
        json.dump(all_posts, f, indent=2)
    
    print(f"✅ Saved {len(all_posts)} posts to {filename}")
    return filename

if __name__ == "__main__":
    collect_sample_data()
    