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
            user_agent=os.getenv('REDDIT_USER_AGENT', 'abuse-tracker-v1.0')
        )
        
        # Test connection
        try:
            self.reddit.user.me()
            logger.info("✅ Reddit API connection successful")
        except Exception as e:
            logger.error(f"❌ Reddit API connection failed: {e}")
            raise
    
    def get_subreddit_posts(self, subreddit_name: str, limit: int = 100, 
                           time_filter: str = 'day') -> List[Dict]:
        """
        Collect posts from a subreddit
        
        Args:
            subreddit_name: Name of the subreddit (without r/)
            limit: Number of posts to collect
            time_filter: Time filter (hour, day, week, month, year, all)
            
        Returns:
            List of post dictionaries
        """
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
    
    def get_post_comments(self, post_id: str, limit: int = 100) -> List[Dict]:
        """
        Collect comments from a specific post
        
        Args:
            post_id: Reddit post ID
            limit: Number of comments to collect
            
        Returns:
            List of comment dictionaries
        """
        try:
            submission = self.reddit.submission(id=post_id)
            comments = []
            
            logger.info(f"🔍 Collecting comments from post {post_id}")
            
            # Expand all comments
            submission.comments.replace_more(limit=0)
            
            comment_count = 0
            for comment in submission.comments.list():
                if comment_count >= limit:
                    break
                    
                comment_data = {
                    'id': comment.id,
                    'body': comment.body,
                    'author': str(comment.author) if comment.author else '[deleted]',
                    'subreddit': str(comment.subreddit),
                    'score': comment.score,
                    'created_utc': comment.created_utc,
                    'parent_id': comment.parent_id,
                    'post_id': post_id,
                    'is_submitter': comment.is_submitter
                }
                comments.append(comment_data)
                comment_count += 1
                
                # Be respectful to Reddit's API
                time.sleep(0.1)
            
            logger.info(f"✅ Collected {len(comments)} comments from post {post_id}")
            return comments
            
        except Exception as e:
            logger.error(f"❌ Error collecting comments from post {post_id}: {e}")
            return []
    
    def search_posts(self, query: str, subreddit_name: str = None, 
                     limit: int = 100, time_filter: str = 'week') -> List[Dict]:
        """
        Search for posts containing specific keywords
        
        Args:
            query: Search query
            subreddit_name: Specific subreddit to search (optional)
            limit: Number of posts to return
            time_filter: Time filter for search
            
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
    
    if posts:
        print(f"First post: {posts[0]['title']}")
        
        # Test collecting comments from first post
        comments = client.get_post_comments(posts[0]['id'], limit=3)
        print(f"Collected {len(comments)} comments from first post")
