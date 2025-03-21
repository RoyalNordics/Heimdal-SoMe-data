#!/usr/bin/env python3
"""
Main entry point for the Heimdal SoMe Data application.
"""

import os
import sys
import uvicorn
from dotenv import load_dotenv
from pathlib import Path

# Add the parent directory to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Load environment variables
load_dotenv()

# Get API configuration from environment variables
API_HOST = os.getenv("API_HOST", "0.0.0.0")
# Use PORT env var for compatibility with Render, falling back to API_PORT if available, then 8000
API_PORT = int(os.getenv("PORT", os.getenv("API_PORT", "8000")))

# Initialize the database
from heimdal_data.database.database import init_db

# Initialize the database
init_db()
print("Database initialized")

if __name__ == "__main__":
    print(f"Starting Heimdal SoMe Data API on {API_HOST}:{API_PORT}")
    uvicorn.run(
        "heimdal_data.api.app:app",
        host=API_HOST,
        port=API_PORT,
        reload=True,
        log_level="info"
    )
