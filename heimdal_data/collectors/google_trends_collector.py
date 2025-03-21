import os
import asyncio
import random
from pytrends.request import TrendReq
from typing import Dict, List, Any
from datetime import datetime

from heimdal_data.collectors.base_collector import BaseCollector
from heimdal_data.database.database import SessionLocal
from heimdal_data.database.models import SeoData

class GoogleTrendsCollector(BaseCollector):
    """
    Collector for Google Trends data.
    """
    
    def __init__(self):
        """
        Initialize the Google Trends collector.
        """
        super().__init__("GoogleTrends")
        
        # Initialize PyTrends client
        self.pytrends = self._init_client()
        
        # Default keywords to track if none are provided
        self.default_keywords = [
            "digital marketing",
            "social media marketing",
            "content marketing",
            "SEO",
            "influencer marketing"
        ]
    
    def _init_client(self) -> TrendReq:
        """
        Initialize the PyTrends client.
        
        Returns:
            TrendReq: PyTrends client.
        """
        try:
            # Initialize with English language and Denmark as the geo
            pytrends = TrendReq(hl='en-US', tz=360)
            self.logger.info("PyTrends client initialized successfully")
            return pytrends
        except Exception as e:
            self.logger.exception(f"Error initializing PyTrends client: {e}")
            raise
    
    async def collect(self, keywords: List[str] = None, testing_mode: bool = False) -> List[Dict[str, Any]]:
        """
        Collect search interest data from Google Trends.
        
        Args:
            keywords (List[str], optional): List of keywords to track. Defaults to None.
            testing_mode (bool, optional): Whether to return mock data. Defaults to False.
        
        Returns:
            List[Dict[str, Any]]: List of search interest data for keywords.
        """
        self.logger.info("Collecting search interest data from Google Trends")
        
        # Use default keywords if none are provided
        if not keywords:
            keywords = self.default_keywords
        
        # List to store the collected data
        trends_data = []
        
        # Check if we're in testing mode
        if testing_mode:
            self.logger.info("Using mock data for Google Trends")
            
            # Generate mock data for each keyword
            for keyword in keywords:
                # Create a data item for this keyword with mock data
                keyword_data = {
                    'keyword': keyword,
                    'trend_score': round(random.uniform(0, 100), 2),  # Random score between 0 and 100
                    'volume': random.randint(1000, 10000),  # Random volume between 1000 and 10000
                    'source': 'Google Trends (Mock)',
                    'timestamp': datetime.now()
                }
                
                trends_data.append(keyword_data)
            
            self.logger.info(f"Generated mock data for {len(trends_data)} keywords")
            return trends_data
        
        try:
            # Use asyncio to run the blocking PyTrends calls in a separate thread
            await asyncio.to_thread(
                self.pytrends.build_payload,
                kw_list=keywords,
                cat=0,  # Category: All categories
                timeframe='now 7-d',  # Last 7 days
                geo='DK',  # Denmark
                gprop=''  # Web search
            )
            
            # Get interest over time
            interest_over_time_df = await asyncio.to_thread(
                self.pytrends.interest_over_time
            )
            
            if interest_over_time_df.empty:
                self.logger.warning("No interest over time data found")
                return []
            
            # Get the latest data point for each keyword
            latest_date = interest_over_time_df.index[-1]
            
            for keyword in keywords:
                if keyword in interest_over_time_df.columns:
                    trend_score = float(interest_over_time_df[keyword].iloc[-1])
                    
                    # Get related queries for volume estimation
                    related_queries = await asyncio.to_thread(
                        self.pytrends.related_queries
                    )
                    
                    # Estimate volume based on related queries (this is a rough approximation)
                    volume = 0
                    if keyword in related_queries and 'top' in related_queries[keyword]:
                        top_df = related_queries[keyword]['top']
                        if not top_df.empty:
                            # Sum the values of related queries as a rough volume estimate
                            volume = int(top_df['value'].sum())
                    
                    # Create a data item for this keyword
                    keyword_data = {
                        'keyword': keyword,
                        'trend_score': trend_score,
                        'volume': volume,
                        'source': 'Google Trends',
                        'timestamp': datetime.now()
                    }
                    
                    trends_data.append(keyword_data)
            
            self.logger.info(f"Collected search interest data for {len(trends_data)} keywords from Google Trends")
            return trends_data
        
        except Exception as e:
            self.logger.exception(f"Error collecting search interest data from Google Trends: {e}")
            
            # If we encounter an error, return mock data
            self.logger.info("Falling back to mock data due to error")
            return await self.collect(keywords, testing_mode=True)
    
    async def save(self, data: List[Dict[str, Any]]) -> bool:
        """
        Save the collected Google Trends data to the database.
        
        Args:
            data (List[Dict[str, Any]]): List of search interest data to save.
            
        Returns:
            bool: True if the data was saved successfully, False otherwise.
        """
        self.logger.info(f"Saving {len(data)} keywords to database")
        
        try:
            # Create a database session
            db = SessionLocal()
            
            # Save each keyword to the database
            for keyword_data in data:
                seo_data = SeoData(
                    keyword=keyword_data['keyword'],
                    trend_score=keyword_data['trend_score'],
                    volume=keyword_data['volume'],
                    source=keyword_data['source'],
                    timestamp=keyword_data['timestamp']
                )
                
                db.add(seo_data)
            
            # Commit the changes
            db.commit()
            
            # Close the session
            db.close()
            
            self.logger.info(f"Successfully saved {len(data)} keywords to database")
            return True
        
        except Exception as e:
            self.logger.exception(f"Error saving keywords to database: {e}")
            
            # Rollback the session in case of error
            if 'db' in locals():
                db.rollback()
                db.close()
            
            return False
