#!/usr/bin/env python3
"""
Script to generate mock data for the Heimdal SoMe Data Collection module.
"""

import os
import sys
import random
import argparse
from datetime import datetime, timedelta
from pathlib import Path

# Add the parent directory to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Import the database models
from heimdal_data.database.database import SessionLocal, engine
from heimdal_data.database.models import Base, HashtagTrend, SocialEngagement, SeoData

def generate_hashtag_trends(db, count=20, platforms=None):
    """
    Generate mock hashtag trends data.
    
    Args:
        db: Database session
        count (int): Number of hashtag trends to generate
        platforms (list): List of platforms to generate data for
    """
    if platforms is None:
        platforms = ["Twitter", "TikTok"]
    
    popular_hashtags = [
        "digitalmarketing", "socialmedia", "marketing", "business", "instagram",
        "seo", "branding", "contentmarketing", "entrepreneur", "smallbusiness",
        "startup", "success", "motivation", "leadership", "innovation",
        "technology", "ai", "machinelearning", "datascience", "python",
        "javascript", "webdevelopment", "coding", "programming", "developer",
        "design", "ux", "ui", "graphicdesign", "webdesign"
    ]
    
    print(f"Generating {count} hashtag trends...")
    
    for i in range(count):
        # Generate a random timestamp within the last 7 days
        timestamp = datetime.now() - timedelta(
            days=random.randint(0, 7),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59)
        )
        
        # Select a random platform and hashtag
        platform = random.choice(platforms)
        hashtag = random.choice(popular_hashtags)
        
        # Generate a random engagement value
        engagement = random.randint(1000, 100000)
        
        # Create a hashtag trend
        hashtag_trend = HashtagTrend(
            platform=platform,
            hashtag=hashtag,
            engagement=engagement,
            timestamp=timestamp
        )
        
        # Add to the database
        db.add(hashtag_trend)
    
    # Commit the changes
    db.commit()
    print(f"Generated {count} hashtag trends")

def generate_social_engagement(db, count=20, platforms=None):
    """
    Generate mock social engagement data.
    
    Args:
        db: Database session
        count (int): Number of social engagement records to generate
        platforms (list): List of platforms to generate data for
    """
    if platforms is None:
        platforms = ["Twitter", "Facebook", "TikTok"]
    
    post_types = ["text", "image", "video", "link", "poll"]
    
    content_snippets = [
        "Check out our new product!",
        "We're excited to announce our latest feature.",
        "Join us for our upcoming webinar.",
        "Learn how to improve your marketing strategy.",
        "Tips and tricks for better social media engagement.",
        "How to grow your business with digital marketing.",
        "The future of AI in marketing.",
        "Why content marketing is important for your business.",
        "How to use social media to grow your brand.",
        "The importance of SEO for your website."
    ]
    
    print(f"Generating {count} social engagement records...")
    
    for i in range(count):
        # Generate a random timestamp within the last 7 days
        timestamp = datetime.now() - timedelta(
            days=random.randint(0, 7),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59)
        )
        
        # Select a random platform, post type, and content snippet
        platform = random.choice(platforms)
        post_type = random.choice(post_types)
        content_snippet = random.choice(content_snippets)
        
        # Generate random engagement metrics
        likes = random.randint(10, 1000)
        comments = random.randint(0, 100)
        shares = random.randint(0, 50)
        reach = random.randint(100, 10000)
        
        # Generate a random post ID
        post_id = f"{platform.lower()}_post_{random.randint(1000, 9999)}"
        
        # Create a social engagement record
        social_engagement = SocialEngagement(
            platform=platform,
            post_type=post_type,
            post_id=post_id,
            likes=likes,
            comments=comments,
            shares=shares,
            reach=reach,
            content_snippet=content_snippet,
            timestamp=timestamp
        )
        
        # Add to the database
        db.add(social_engagement)
    
    # Commit the changes
    db.commit()
    print(f"Generated {count} social engagement records")

def generate_seo_data(db, count=20):
    """
    Generate mock SEO data.
    
    Args:
        db: Database session
        count (int): Number of SEO data records to generate
    """
    keywords = [
        "digital marketing", "social media marketing", "content marketing",
        "SEO", "search engine optimization", "PPC", "pay per click",
        "email marketing", "influencer marketing", "affiliate marketing",
        "brand awareness", "lead generation", "conversion rate optimization",
        "marketing automation", "customer acquisition", "customer retention",
        "marketing strategy", "market research", "competitive analysis",
        "target audience", "buyer persona", "customer journey", "sales funnel",
        "ROI", "KPI", "analytics", "data-driven marketing", "growth hacking",
        "viral marketing", "guerrilla marketing"
    ]
    
    print(f"Generating {count} SEO data records...")
    
    for i in range(count):
        # Generate a random timestamp within the last 7 days
        timestamp = datetime.now() - timedelta(
            days=random.randint(0, 7),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59)
        )
        
        # Select a random keyword
        keyword = random.choice(keywords)
        
        # Generate random SEO metrics
        trend_score = round(random.uniform(0, 100), 2)
        volume = random.randint(1000, 10000)
        difficulty = round(random.uniform(0, 100), 2)
        cpc = round(random.uniform(0.1, 10.0), 2)
        competition = round(random.uniform(0, 1), 2)
        
        # Create an SEO data record
        seo_data = SeoData(
            keyword=keyword,
            trend_score=trend_score,
            volume=volume,
            difficulty=difficulty,
            cpc=cpc,
            competition=competition,
            source="Mock Data Generator",
            timestamp=timestamp
        )
        
        # Add to the database
        db.add(seo_data)
    
    # Commit the changes
    db.commit()
    print(f"Generated {count} SEO data records")

def main():
    """
    Main function.
    """
    parser = argparse.ArgumentParser(description="Generate mock data for the Heimdal SoMe Data Collection module")
    parser.add_argument("--hashtag-trends", type=int, default=20, help="Number of hashtag trends to generate")
    parser.add_argument("--social-engagement", type=int, default=20, help="Number of social engagement records to generate")
    parser.add_argument("--seo-data", type=int, default=20, help="Number of SEO data records to generate")
    parser.add_argument("--init-db", action="store_true", help="Initialize the database tables")
    
    args = parser.parse_args()
    
    # Initialize the database tables if requested
    if args.init_db:
        print("Initializing database tables...")
        Base.metadata.create_all(engine)
        print("Database tables initialized successfully")
    
    print("Generating mock data...")
    
    # Create a database session
    db = SessionLocal()
    
    try:
        # Generate mock data
        generate_hashtag_trends(db, args.hashtag_trends)
        generate_social_engagement(db, args.social_engagement)
        generate_seo_data(db, args.seo_data)
        
        print("Mock data generation completed successfully")
    except Exception as e:
        print(f"Error generating mock data: {e}")
    finally:
        # Close the session
        db.close()

if __name__ == "__main__":
    main()
