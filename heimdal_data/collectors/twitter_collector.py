import os
import tweepy
import asyncio
from typing import Dict, List, Any
from datetime import datetime
from sqlalchemy.orm import Session

from heimdal_data.collectors.base_collector import BaseCollector
from heimdal_data.database.database import SessionLocal
from heimdal_data.database.models import HashtagTrend

class TwitterCollector(BaseCollector):
    """
    Collector for Twitter data.
    """
    
    def __init__(self):
        """
        Initialize the Twitter collector.
        """
        super().__init__("Twitter")
        
        # Get Twitter API credentials from environment variables
        self.api_key = os.getenv("TWITTER_API_KEY")
        self.api_secret = os.getenv("TWITTER_API_SECRET")
        self.access_token = os.getenv("TWITTER_ACCESS_TOKEN")
        self.access_secret = os.getenv("TWITTER_ACCESS_SECRET")
        self.bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
        
        if not all([self.api_key, self.api_secret, self.access_token, self.access_secret, self.bearer_token]):
            self.logger.error("Twitter API credentials not found in environment variables")
            raise ValueError("Twitter API credentials not found in environment variables")
        
        # Initialize Twitter API client
        self.client = self._init_client()
    
    def _init_client(self) -> tweepy.Client:
        """
        Initialize the Twitter API client.
        
        Returns:
            tweepy.Client: Twitter API client.
        """
        try:
            client = tweepy.Client(
                bearer_token=self.bearer_token,
                consumer_key=self.api_key,
                consumer_secret=self.api_secret,
                access_token=self.access_token,
                access_token_secret=self.access_secret
            )
            self.logger.info("Twitter API client initialized successfully")
            return client
        except Exception as e:
            self.logger.exception(f"Error initializing Twitter API client: {e}")
            raise
    
    async def collect(self) -> List[Dict[str, Any]]:
        """
        Collect trending hashtags from Twitter.
        
        Returns:
            List[Dict[str, Any]]: List of trending hashtags with engagement data.
        """
        self.logger.info("Collecting trending hashtags from Twitter")
        
        # List to store the collected data
        hashtags_data = []
        
        try:
            # Get available trend locations (WOEIDs)
            # For simplicity, we'll use the worldwide trends (WOEID 1)
            woeid = 1  # Worldwide
            
            # Use asyncio to run the blocking Tweepy calls in a separate thread
            trends = await asyncio.to_thread(
                self.client.get_place_trends, id=woeid
            )
            
            if not trends or not trends.data:
                self.logger.warning("No trending topics found")
                return []
            
            # Process each trending topic
            for trend in trends.data:
                # Skip non-hashtag trends
                if not trend['name'].startswith('#'):
                    continue
                
                hashtag = trend['name'].lstrip('#')
                tweet_volume = trend.get('tweet_volume', 0)
                
                # Create a data item for this hashtag
                hashtag_data = {
                    'platform': 'Twitter',
                    'hashtag': hashtag,
                    'engagement': tweet_volume if tweet_volume else 0,
                    'timestamp': datetime.now()
                }
                
                hashtags_data.append(hashtag_data)
            
            self.logger.info(f"Collected {len(hashtags_data)} trending hashtags from Twitter")
            return hashtags_data
        
        except Exception as e:
            self.logger.exception(f"Error collecting trending hashtags from Twitter: {e}")
            return []
    
    async def save(self, data: List[Dict[str, Any]]) -> bool:
        """
        Save the collected Twitter data to the database.
        
        Args:
            data (List[Dict[str, Any]]): List of hashtag data to save.
            
        Returns:
            bool: True if the data was saved successfully, False otherwise.
        """
        self.logger.info(f"Saving {len(data)} hashtags to database")
        
        try:
            # Create a database session
            db = SessionLocal()
            
            # Save each hashtag to the database
            for hashtag_data in data:
                hashtag_trend = HashtagTrend(
                    platform=hashtag_data['platform'],
                    hashtag=hashtag_data['hashtag'],
                    engagement=hashtag_data['engagement'],
                    timestamp=hashtag_data['timestamp']
                )
                
                db.add(hashtag_trend)
            
            # Commit the changes
            db.commit()
            
            # Close the session
            db.close()
            
            self.logger.info(f"Successfully saved {len(data)} hashtags to database")
            return True
        
        except Exception as e:
            self.logger.exception(f"Error saving hashtags to database: {e}")
            
            # Rollback the session in case of error
            if 'db' in locals():
                db.rollback()
                db.close()
            
            return False
