import os
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from dotenv import load_dotenv
import logging

from heimdal_data.api.routes import router as data_router, initialize_collectors, fetch_data_task
from heimdal_data.database.database import init_db, check_db_connection

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("api.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("api")

# Create FastAPI app
app = FastAPI(
    title="Heimdal SoMe Data API",
    description="API for accessing social media and SEO data collected by Heimdal",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Include routers
app.include_router(data_router)

# Create scheduler
scheduler = AsyncIOScheduler()

@app.on_event("startup")
async def startup_event():
    """
    Event handler for application startup.
    """
    logger.info("Starting up the application")
    
    # Initialize the database
    try:
        init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
    
    # Check database connection
    if check_db_connection():
        logger.info("Database connection successful")
    else:
        logger.error("Database connection failed")
    
    # Initialize collectors
    try:
        initialize_collectors()
        logger.info("Collectors initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing collectors: {e}")
    
    # Set up scheduler for automated data collection
    try:
        # Get the schedule from environment variables or use default (daily at midnight)
        schedule = os.getenv("DATA_COLLECTION_SCHEDULE", "0 0 * * *")
        
        # Add the data collection job to the scheduler
        scheduler.add_job(
            fetch_data_task,
            CronTrigger.from_crontab(schedule),
            id="data_collection",
            replace_existing=True
        )
        
        # Start the scheduler
        scheduler.start()
        logger.info(f"Scheduler started with schedule: {schedule}")
    except Exception as e:
        logger.error(f"Error setting up scheduler: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    """
    Event handler for application shutdown.
    """
    logger.info("Shutting down the application")
    
    # Shut down the scheduler
    if scheduler.running:
        scheduler.shutdown()
        logger.info("Scheduler shut down")

@app.get("/")
async def root():
    """
    Root endpoint.
    """
    return {
        "message": "Welcome to the Heimdal SoMe Data API",
        "version": "1.0.0",
        "endpoints": [
            "/api/data/trends",
            "/api/data/engagement",
            "/api/data/seo",
            "/api/data/fetch"
        ]
    }

@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    """
    # Check database connection
    db_status = "ok" if check_db_connection() else "error"
    
    return {
        "status": "ok",
        "database": db_status,
        "scheduler": "ok" if scheduler.running else "error"
    }
