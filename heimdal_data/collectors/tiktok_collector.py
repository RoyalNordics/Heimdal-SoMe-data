import os
import asyncio
import requests
from typing import Dict, List, Any
from datetime import datetime

from heimdal_data.collectors.base_collector import BaseCollector
from heimdal_data.database.database import SessionLocal
from heimdal_data.database.models import HashtagTrend, SocialEngagement

class TikTokCollector(BaseCollector):
    """
    Collector for TikTok data.
    """
    
    def __init__(self):
        """
        Initialize the TikTok collector.
        """
        super().__init__("TikTok")
        
        # Get TikTok API credentials from environment variables
        self.api_key = os.getenv("TIKTOK_API_KEY")
        self.api_secret = os.getenv("TIKTOK_API_SECRET")
        
        if not all([self.api_key, self.api_secret]):
            self.logger.error("TikTok API credentials not found in environment variables")
            raise ValueError("TikTok API credentials not found in environment variables")
        
        # Base URL for TikTok API
        self.base_url = "https://open-api.tiktok.com/api/v2"
        
        # Headers for API requests
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
    
    async def collect_trending_hashtags(self) -> List[Dict[str, Any]]:
        """
        Collect trending hashtags from TikTok.
        
        Returns:
            List[Dict[str, Any]]: List of trending hashtags with engagement data.
        """
        self.logger.info("Collecting trending hashtags from TikTok")
        
        # List to store the collected data
        hashtags_data = []
        
        try:
            # Use asyncio to run the blocking requests in a separate thread
            # Note: This is a simulated endpoint, as TikTok's API structure may differ
            response = await asyncio.to_thread(
                requests.get,
                f"{self.base_url}/hashtag/trending",
                headers=self.headers
            )
            
            if response.status_code != 200:
                self.logger.error(f"Error from TikTok API: {response.status_code} - {response.text}")
                return []
            
            data = response.json()
            
            if not data or 'data' not in data or 'hashtags' not in data['data']:
                self.logger.warning("No trending hashtags found")
                return []
            
            # Process each trending hashtag
            for hashtag in data['data']['hashtags']:
                hashtag_name = hashtag.get('name', '')
                view_count = hashtag.get('view_count', 0)
                video_count = hashtag.get('video_count', 0)
                
                # Calculate engagement as a combination of views and videos
                engagement = view_count + (video_count * 100)  # Weighting videos more heavily
                
                # Create a data item for this hashtag
                hashtag_data = {
                    'platform': 'TikTok',
                    'hashtag': hashtag_name,
                    'engagement': engagement,
                    'timestamp': datetime.now()
                }
                
                hashtags_data.append(hashtag_data)
            
            self.logger.info(f"Collected {len(hashtags_data)} trending hashtags from TikTok")
            return hashtags_data
        
        except Exception as e:
            self.logger.exception(f"Error collecting trending hashtags from TikTok: {e}")
            return []
    
    async def collect_engagement_data(self) -> List[Dict[str, Any]]:
        """
        Collect engagement data from TikTok videos.
        
        Returns:
            List[Dict[str, Any]]: List of engagement data from TikTok videos.
        """
        self.logger.info("Collecting engagement data from TikTok videos")
        
        # List to store the collected data
        engagement_data = []
        
        try:
            # Use asyncio to run the blocking requests in a separate thread
            # Note: This is a simulated endpoint, as TikTok's API structure may differ
            response = await asyncio.to_thread(
                requests.get,
                f"{self.base_url}/video/list",
                headers=self.headers,
                params={"count": 20, "cursor": 0}  # Get the latest 20 videos
            )
            
            if response.status_code != 200:
                self.logger.error(f"Error from TikTok API: {response.status_code} - {response.text}")
                return []
            
            data = response.json()
            
            if not data or 'data' not in data or 'videos' not in data['data']:
                self.logger.warning("No videos found")
                return []
            
            # Process each video
            for video in data['data']['videos']:
                video_id = video.get('id', '')
                description = video.get('description', '')
                
                # Get engagement metrics
                likes = video.get('like_count', 0)
                comments = video.get('comment_count', 0)
                shares = video.get('share_count', 0)
                views = video.get('view_count', 0)
                
                # Create a data item for this video
                video_data = {
                    'platform': 'TikTok',
                    'post_type': 'video',
                    'post_id': video_id,
                    'likes': likes,
                    'comments': comments,
                    'shares': shares,
                    'reach': views,
                    'content_snippet': description[:255] if description else '',
                    'timestamp': datetime.now()
                }
                
                engagement_data.append(video_data)
            
            self.logger.info(f"Collected engagement data from {len(engagement_data)} TikTok videos")
            return engagement_data
        
        except Exception as e:
            self.logger.exception(f"Error collecting engagement data from TikTok videos: {e}")
            return []
    
    async def collect(self) -> List[Dict[str, Any]]:
        """
        Collect data from TikTok.
        
        Returns:
            List[Dict[str, Any]]: List of collected data.
        """
        self.logger.info("Collecting data from TikTok")
        
        # Collect trending hashtags
        hashtags_data = await self.collect_trending_hashtags()
        
        # Collect engagement data
        engagement_data = await self.collect_engagement_data()
        
        # Return both types of data
        return {
            'hashtags': hashtags_data,
            'engagement': engagement_data
        }
    
    async def save(self, data: Dict[str, List[Dict[str, Any]]]) -> bool:
        """
        Save the collected TikTok data to the database.
        
        Args:
            data (Dict[str, List[Dict[str, Any]]]): Dictionary containing hashtags and engagement data.
            
        Returns:
            bool: True if the data was saved successfully, False otherwise.
        """
        self.logger.info("Saving TikTok data to database")
        
        try:
            # Create a database session
            db = SessionLocal()
            
            # Save hashtags data
            if 'hashtags' in data and data['hashtags']:
                self.logger.info(f"Saving {len(data['hashtags'])} hashtags to database")
                
                for hashtag_data in data['hashtags']:
                    hashtag_trend = HashtagTrend(
                        platform=hashtag_data['platform'],
                        hashtag=hashtag_data['hashtag'],
                        engagement=hashtag_data['engagement'],
                        timestamp=hashtag_data['timestamp']
                    )
                    
                    db.add(hashtag_trend)
            
            # Save engagement data
            if 'engagement' in data and data['engagement']:
                self.logger.info(f"Saving {len(data['engagement'])} videos to database")
                
                for video_data in data['engagement']:
                    social_engagement = SocialEngagement(
                        platform=video_data['platform'],
                        post_type=video_data['post_type'],
                        post_id=video_data['post_id'],
                        likes=video_data['likes'],
                        comments=video_data['comments'],
                        shares=video_data['shares'],
                        reach=video_data['reach'],
                        content_snippet=video_data['content_snippet'],
                        timestamp=video_data['timestamp']
                    )
                    
                    db.add(social_engagement)
            
            # Commit the changes
            db.commit()
            
            # Close the session
            db.close()
            
            self.logger.info("Successfully saved TikTok data to database")
            return True
        
        except Exception as e:
            self.logger.exception(f"Error saving TikTok data to database: {e}")
            
            # Rollback the session in case of error
            if 'db' in locals():
                db.rollback()
                db.close()
            
            return False
