import os
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Dict, Any
import asyncio
from datetime import datetime, timedelta

from heimdal_data.database.database import get_db
from heimdal_data.database.models import HashtagTrend, SocialEngagement, SeoData
from heimdal_data.collectors.twitter_collector import TwitterCollector
from heimdal_data.collectors.facebook_collector import FacebookCollector
from heimdal_data.collectors.tiktok_collector import TikTokCollector
from heimdal_data.collectors.google_trends_collector import GoogleTrendsCollector

# Create API router
router = APIRouter(prefix="/api/data", tags=["data"])

# Create collectors
twitter_collector = None
facebook_collector = None
tiktok_collector = None
google_trends_collector = None

def initialize_collectors():
    """
    Initialize all collectors.
    """
    global twitter_collector, facebook_collector, tiktok_collector, google_trends_collector
    
    # Check if API keys are placeholders
    twitter_api_key = os.getenv("TWITTER_API_KEY", "")
    facebook_app_id = os.getenv("FACEBOOK_APP_ID", "")
    tiktok_api_key = os.getenv("TIKTOK_API_KEY", "")
    
    is_twitter_placeholder = twitter_api_key.startswith("placeholder")
    is_facebook_placeholder = facebook_app_id.startswith("placeholder")
    is_tiktok_placeholder = tiktok_api_key.startswith("placeholder")
    
    # Initialize collectors if API keys are not placeholders
    if not is_twitter_placeholder:
        try:
            twitter_collector = TwitterCollector()
            print("Twitter collector initialized successfully")
        except Exception as e:
            print(f"Error initializing Twitter collector: {e}")
    else:
        print("Twitter collector not initialized: API keys are placeholders")
    
    if not is_facebook_placeholder:
        try:
            facebook_collector = FacebookCollector()
            print("Facebook collector initialized successfully")
        except Exception as e:
            print(f"Error initializing Facebook collector: {e}")
    else:
        print("Facebook collector not initialized: API keys are placeholders")
    
    if not is_tiktok_placeholder:
        try:
            tiktok_collector = TikTokCollector()
            print("TikTok collector initialized successfully")
        except Exception as e:
            print(f"Error initializing TikTok collector: {e}")
    else:
        print("TikTok collector not initialized: API keys are placeholders")
    
    # Google Trends doesn't require API keys, so we can always initialize it
    try:
        google_trends_collector = GoogleTrendsCollector()
        print("Google Trends collector initialized successfully")
    except Exception as e:
        print(f"Error initializing Google Trends collector: {e}")

@router.get("/trends", response_model=List[Dict[str, Any]])
async def get_trends(db: Session = Depends(get_db), limit: int = 50, days: int = 7):
    """
    Get the latest hashtag trends.
    
    Args:
        db (Session): Database session.
        limit (int, optional): Maximum number of trends to return. Defaults to 50.
        days (int, optional): Number of days to look back. Defaults to 7.
    
    Returns:
        List[Dict[str, Any]]: List of hashtag trends.
    """
    # Calculate the date limit
    date_limit = datetime.now() - timedelta(days=days)
    
    # Query the database for hashtag trends
    trends = db.query(HashtagTrend).filter(
        HashtagTrend.timestamp >= date_limit
    ).order_by(
        HashtagTrend.engagement.desc()
    ).limit(limit).all()
    
    # Convert to dictionary
    result = []
    for trend in trends:
        result.append({
            "id": trend.id,
            "platform": trend.platform,
            "hashtag": trend.hashtag,
            "engagement": trend.engagement,
            "timestamp": trend.timestamp.isoformat()
        })
    
    return result

@router.get("/engagement", response_model=List[Dict[str, Any]])
async def get_engagement(db: Session = Depends(get_db), limit: int = 50, days: int = 7):
    """
    Get the latest engagement statistics.
    
    Args:
        db (Session): Database session.
        limit (int, optional): Maximum number of engagement records to return. Defaults to 50.
        days (int, optional): Number of days to look back. Defaults to 7.
    
    Returns:
        List[Dict[str, Any]]: List of engagement statistics.
    """
    # Calculate the date limit
    date_limit = datetime.now() - timedelta(days=days)
    
    # Query the database for engagement statistics
    engagements = db.query(SocialEngagement).filter(
        SocialEngagement.timestamp >= date_limit
    ).order_by(
        SocialEngagement.timestamp.desc()
    ).limit(limit).all()
    
    # Convert to dictionary
    result = []
    for engagement in engagements:
        result.append({
            "id": engagement.id,
            "platform": engagement.platform,
            "post_type": engagement.post_type,
            "post_id": engagement.post_id,
            "likes": engagement.likes,
            "comments": engagement.comments,
            "shares": engagement.shares,
            "reach": engagement.reach,
            "content_snippet": engagement.content_snippet,
            "timestamp": engagement.timestamp.isoformat()
        })
    
    return result

@router.get("/seo", response_model=List[Dict[str, Any]])
async def get_seo_data(db: Session = Depends(get_db), limit: int = 50, days: int = 7):
    """
    Get the latest SEO data.
    
    Args:
        db (Session): Database session.
        limit (int, optional): Maximum number of SEO records to return. Defaults to 50.
        days (int, optional): Number of days to look back. Defaults to 7.
    
    Returns:
        List[Dict[str, Any]]: List of SEO data.
    """
    # Calculate the date limit
    date_limit = datetime.now() - timedelta(days=days)
    
    # Query the database for SEO data
    seo_data = db.query(SeoData).filter(
        SeoData.timestamp >= date_limit
    ).order_by(
        SeoData.trend_score.desc()
    ).limit(limit).all()
    
    # Convert to dictionary
    result = []
    for data in seo_data:
        result.append({
            "id": data.id,
            "keyword": data.keyword,
            "trend_score": data.trend_score,
            "volume": data.volume,
            "difficulty": data.difficulty,
            "cpc": data.cpc,
            "competition": data.competition,
            "source": data.source,
            "timestamp": data.timestamp.isoformat()
        })
    
    return result

async def fetch_data_task():
    """
    Background task to fetch data from all sources.
    """
    print("Starting data collection task...")
    
    # Initialize collectors if not already initialized
    if twitter_collector is None or facebook_collector is None or tiktok_collector is None or google_trends_collector is None:
        initialize_collectors()
    
    # Collect data from Twitter
    if twitter_collector:
        try:
            await twitter_collector.run()
        except Exception as e:
            print(f"Error collecting data from Twitter: {e}")
    
    # Collect data from Facebook
    if facebook_collector:
        try:
            await facebook_collector.run()
        except Exception as e:
            print(f"Error collecting data from Facebook: {e}")
    
    # Collect data from TikTok
    if tiktok_collector:
        try:
            await tiktok_collector.run()
        except Exception as e:
            print(f"Error collecting data from TikTok: {e}")
    
    # Collect data from Google Trends
    if google_trends_collector:
        try:
            # Use testing mode for Google Trends since it doesn't require API keys
            # but might still fail if we try to make real API calls
            data = await google_trends_collector.collect(testing_mode=True)
            if data:
                await google_trends_collector.save(data)
                print(f"Successfully collected and saved {len(data)} items from Google Trends")
            else:
                print("No data collected from Google Trends")
        except Exception as e:
            print(f"Error collecting data from Google Trends: {e}")
    
    print("Data collection task completed.")

@router.post("/fetch", response_model=Dict[str, Any])
async def fetch_data(background_tasks: BackgroundTasks):
    """
    Trigger a manual data collection.
    
    Args:
        background_tasks (BackgroundTasks): FastAPI background tasks.
    
    Returns:
        Dict[str, Any]: Status of the data collection task.
    """
    # Add the data collection task to the background tasks
    background_tasks.add_task(fetch_data_task)
    
    return {
        "status": "success",
        "message": "Data collection task started in the background."
    }
