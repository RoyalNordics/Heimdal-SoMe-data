from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class HashtagTrend(Base):
    """
    Model for storing trending hashtags from various social media platforms.
    """
    __tablename__ = "hashtag_trends"

    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String(50), nullable=False, index=True)  # Twitter, Facebook, TikTok, etc.
    hashtag = Column(String(255), nullable=False, index=True)
    engagement = Column(Integer, nullable=False)  # Number of posts, tweets, etc.
    engagement_rate = Column(Float, nullable=True)  # Engagement rate as a percentage
    volume = Column(Integer, nullable=True)  # Volume of posts
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    def __repr__(self):
        return f"<HashtagTrend(platform='{self.platform}', hashtag='{self.hashtag}', engagement={self.engagement})>"


class SocialEngagement(Base):
    """
    Model for storing engagement data from social media posts.
    """
    __tablename__ = "social_engagement"

    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String(50), nullable=False, index=True)  # Twitter, Facebook, TikTok, etc.
    post_type = Column(String(50), nullable=False)  # Text, Image, Video, etc.
    post_id = Column(String(255), nullable=True)  # ID of the post if available
    likes = Column(Integer, nullable=True)
    comments = Column(Integer, nullable=True)
    shares = Column(Integer, nullable=True)
    reach = Column(Integer, nullable=True)  # Number of people who saw the post
    impressions = Column(Integer, nullable=True)  # Number of times the post was displayed
    content_snippet = Column(Text, nullable=True)  # Short snippet of the content
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    def __repr__(self):
        return f"<SocialEngagement(platform='{self.platform}', post_type='{self.post_type}', likes={self.likes})>"


class SeoData(Base):
    """
    Model for storing SEO data for keywords.
    """
    __tablename__ = "seo_data"

    id = Column(Integer, primary_key=True, index=True)
    keyword = Column(String(255), nullable=False, index=True)
    trend_score = Column(Float, nullable=True)  # Score indicating how trending the keyword is
    volume = Column(Integer, nullable=True)  # Search volume
    difficulty = Column(Float, nullable=True)  # SEO difficulty score
    cpc = Column(Float, nullable=True)  # Cost per click
    competition = Column(Float, nullable=True)  # Competition level
    source = Column(String(50), nullable=False)  # Google Trends, Ahrefs, Moz, etc.
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    def __repr__(self):
        return f"<SeoData(keyword='{self.keyword}', trend_score={self.trend_score}, volume={self.volume})>"
