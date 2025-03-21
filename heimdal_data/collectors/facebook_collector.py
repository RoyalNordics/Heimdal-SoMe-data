import os
import asyncio
import facebook
import requests
from typing import Dict, List, Any
from datetime import datetime

from heimdal_data.collectors.base_collector import BaseCollector
from heimdal_data.database.database import SessionLocal
from heimdal_data.database.models import SocialEngagement

class FacebookCollector(BaseCollector):
    """
    Collector for Facebook data.
    """
    
    def __init__(self):
        """
        Initialize the Facebook collector.
        """
        super().__init__("Facebook")
        
        # Get Facebook API credentials from environment variables
        self.app_id = os.getenv("FACEBOOK_APP_ID")
        self.app_secret = os.getenv("FACEBOOK_APP_SECRET")
        self.access_token = os.getenv("FACEBOOK_ACCESS_TOKEN")
        
        if not all([self.app_id, self.app_secret, self.access_token]):
            self.logger.error("Facebook API credentials not found in environment variables")
            raise ValueError("Facebook API credentials not found in environment variables")
        
        # Initialize Facebook API client
        self.graph = self._init_client()
    
    def _init_client(self) -> facebook.GraphAPI:
        """
        Initialize the Facebook Graph API client.
        
        Returns:
            facebook.GraphAPI: Facebook Graph API client.
        """
        try:
            graph = facebook.GraphAPI(access_token=self.access_token, version="3.1")
            self.logger.info("Facebook Graph API client initialized successfully")
            return graph
        except Exception as e:
            self.logger.exception(f"Error initializing Facebook Graph API client: {e}")
            raise
    
    async def collect(self) -> List[Dict[str, Any]]:
        """
        Collect engagement data from Facebook.
        
        Returns:
            List[Dict[str, Any]]: List of engagement data from Facebook posts.
        """
        self.logger.info("Collecting engagement data from Facebook")
        
        # List to store the collected data
        engagement_data = []
        
        try:
            # Use asyncio to run the blocking Facebook API calls in a separate thread
            # For this example, we'll get posts from a public page
            # You would need to replace 'meta' with the page ID or name you want to fetch
            page_id = 'meta'
            
            # Get the page posts
            posts = await asyncio.to_thread(
                self.graph.get_connections,
                id=page_id,
                connection_name='posts',
                fields='id,message,created_time,type,shares,likes.summary(true),comments.summary(true)'
            )
            
            if not posts or 'data' not in posts:
                self.logger.warning("No posts found")
                return []
            
            # Process each post
            for post in posts['data']:
                post_id = post.get('id')
                post_type = post.get('type', 'unknown')
                message = post.get('message', '')
                created_time = post.get('created_time')
                
                # Get engagement metrics
                likes = post.get('likes', {}).get('summary', {}).get('total_count', 0)
                comments = post.get('comments', {}).get('summary', {}).get('total_count', 0)
                shares = post.get('shares', {}).get('count', 0) if 'shares' in post else 0
                
                # Create a data item for this post
                post_data = {
                    'platform': 'Facebook',
                    'post_type': post_type,
                    'post_id': post_id,
                    'likes': likes,
                    'comments': comments,
                    'shares': shares,
                    'content_snippet': message[:255] if message else '',
                    'timestamp': datetime.now()
                }
                
                engagement_data.append(post_data)
            
            self.logger.info(f"Collected engagement data from {len(engagement_data)} Facebook posts")
            return engagement_data
        
        except Exception as e:
            self.logger.exception(f"Error collecting engagement data from Facebook: {e}")
            return []
    
    async def save(self, data: List[Dict[str, Any]]) -> bool:
        """
        Save the collected Facebook data to the database.
        
        Args:
            data (List[Dict[str, Any]]): List of engagement data to save.
            
        Returns:
            bool: True if the data was saved successfully, False otherwise.
        """
        self.logger.info(f"Saving {len(data)} Facebook posts to database")
        
        try:
            # Create a database session
            db = SessionLocal()
            
            # Save each post to the database
            for post_data in data:
                social_engagement = SocialEngagement(
                    platform=post_data['platform'],
                    post_type=post_data['post_type'],
                    post_id=post_data['post_id'],
                    likes=post_data['likes'],
                    comments=post_data['comments'],
                    shares=post_data['shares'],
                    content_snippet=post_data['content_snippet'],
                    timestamp=post_data['timestamp']
                )
                
                db.add(social_engagement)
            
            # Commit the changes
            db.commit()
            
            # Close the session
            db.close()
            
            self.logger.info(f"Successfully saved {len(data)} Facebook posts to database")
            return True
        
        except Exception as e:
            self.logger.exception(f"Error saving Facebook posts to database: {e}")
            
            # Rollback the session in case of error
            if 'db' in locals():
                db.rollback()
                db.close()
            
            return False
