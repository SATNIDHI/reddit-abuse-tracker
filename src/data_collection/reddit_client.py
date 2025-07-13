# src/data_collection/reddit_client.py
"""
Reddit API client for collecting posts and comments
"""
import praw
import os
from typing import List, Dict, Optional
from dotenv import load_dotenv
import time
import logging

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RedditClient:
    """Reddit API client for data collection"""
    
    def __init__(self):
        """Initialize Reddit client with API credentials"""
        self.reddit = praw.Reddit(
            client_id=os.getenv('REDDIT_CLIENT_ID'),
            client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
            user_agent=os.getenv('REDDIT_USER_AGENT', 'Inner-Musician-8328')
        )
        
        # Test connection
        try:
            self.reddit.user.me()
            logger.info("✅ Reddit API connection successful")
        except Exception as e:
            logger.error(f"❌ Reddit API connection failed: {e}")
            raise
    
    def get_subreddit_posts(self, subreddit_name: str , limit: int = 100, 
                           time_filter: str = 'day') -> List[Dict]:
       
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            posts = []
            
            logger.info(f"🔍 Collecting posts from r/{subreddit_name}")
            
            # Get top posts from specified time period
            for post in subreddit.top(time_filter=time_filter, limit=limit):
                post_data = {
                    'id': post.id,
                    'title': post.title,
                    'selftext': post.selftext,
                    'author': str(post.author) if post.author else '[deleted]',
                    'subreddit': str(post.subreddit),
                    'score': post.score,
                    'upvote_ratio': post.upvote_ratio,
                    'num_comments': post.num_comments,
                    'created_utc': post.created_utc,
                    'url': post.url,
                    'is_self': post.is_self
                }
                posts.append(post_data)
                
                # Be respectful to Reddit's API
                time.sleep(0.1)
            
            logger.info(f"✅ Collected {len(posts)} posts from r/{subreddit_name}")
            return posts
            
        except Exception as e:
            logger.error(f"❌ Error collecting posts from r/{subreddit_name}: {e}")
            return []
    
    def search_posts(self, query: str, subreddit_name: str  = None, 
                     limit: int = 100, time_filter: str = 'week') -> List[Dict]:
        
        """
        Search for posts containing specific keywords
        
        Args:
            query: bitch
            subreddit_name: IndianTeenagers
            limit: 100
            time_filter: month
            
        Returns:
            List of post dictionaries
        """
        try:
            posts = []
            
            if subreddit_name:
                subreddit = self.reddit.subreddit(subreddit_name)
                logger.info(f"🔍 Searching r/{subreddit_name} for: {query}")
            else:
                subreddit = self.reddit.subreddit('all')
                logger.info(f"🔍 Searching all of Reddit for: {query}")
            
            for post in subreddit.search(query, time_filter=time_filter, limit=limit):
                post_data = {
                    'id': post.id,
                    'title': post.title,
                    'selftext': post.selftext,
                    'author': str(post.author) if post.author else '[deleted]',
                    'subreddit': str(post.subreddit),
                    'score': post.score,
                    'upvote_ratio': post.upvote_ratio,
                    'num_comments': post.num_comments,
                    'created_utc': post.created_utc,
                    'url': post.url,
                    'is_self': post.is_self
                }
                posts.append(post_data)
                
                # Be respectful to Reddit's API
                time.sleep(0.1)
            
            logger.info(f"✅ Found {len(posts)} posts matching: {query}")
            return posts
            
        except Exception as e:
            logger.error(f"❌ Error searching for: {query} - {e}")
            return []

# Test the client
if __name__ == "__main__":
    # Quick test of the Reddit client
    client = RedditClient()
    
    # Test collecting posts
    posts = client.get_subreddit_posts('Python', limit=5)
    print(f"Collected {len(posts)} posts")
    
    # if posts:
    #     print(f"First post: {posts[0]['title']}")
        
    #     # Test collecting comments from first post
    #     comments = client.get_post_comments(posts[0]['id'], limit=3)
    #     print(f"Collected {len(comments)} comments from first post")
