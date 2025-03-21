# Heimdal SoMe Data Collection Module

This module collects and stores data from social media platforms, Google Trends, and SEO platforms. It provides an API for accessing the collected data.

## Features

- **Data Collection**: Automatically collects data from various sources:
  - Twitter API: Trending hashtags and engagement rates
  - Facebook Graph API: Posts, likes, comments
  - TikTok API: Popular hashtags and interaction data
  - Google Trends API: Search interest over time
  - SEO data (optional): SEO scores for hashtags

- **Database Storage**: Stores collected data in a PostgreSQL database:
  - Hashtag trends table
  - Social media engagement table
  - SEO data table

- **API Endpoints**:
  - GET /api/data/trends: Returns latest hashtag trends
  - GET /api/data/engagement: Returns engagement statistics
  - GET /api/data/seo: Returns SEO data
  - POST /api/data/fetch: Triggers a manual data collection

- **Automation**: Scheduled data collection using cron jobs

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd heimdal-some-data
   ```

2. Install the required dependencies:
   ```bash
   pip install -r heimdal_data/requirements.txt
   ```

3. Set up the PostgreSQL database:
   ```bash
   # Create a new PostgreSQL database
   createdb heimdal_some_data
   ```

4. Create a `.env` file based on the `.env.example` file:
   ```bash
   cp heimdal_data/.env.example heimdal_data/.env
   # Edit the .env file with your database credentials and API keys
   ```

## Usage

### Starting the API Server

```bash
cd heimdal_data
python main.py
```

The API server will start on http://localhost:8000 by default.

### API Documentation

Once the server is running, you can access the API documentation at http://localhost:8000/docs.

### Endpoints

- **GET /api/data/trends**: Returns the latest hashtag trends
  - Query parameters:
    - `limit` (optional): Maximum number of trends to return (default: 50)
    - `days` (optional): Number of days to look back (default: 7)

- **GET /api/data/engagement**: Returns engagement statistics
  - Query parameters:
    - `limit` (optional): Maximum number of engagement records to return (default: 50)
    - `days` (optional): Number of days to look back (default: 7)

- **GET /api/data/seo**: Returns SEO data
  - Query parameters:
    - `limit` (optional): Maximum number of SEO records to return (default: 50)
    - `days` (optional): Number of days to look back (default: 7)

- **POST /api/data/fetch**: Triggers a manual data collection
  - This endpoint starts a background task to collect data from all sources

### Automated Data Collection

The module is configured to automatically collect data based on the schedule defined in the `.env` file. By default, it collects data daily at midnight.

## Configuration

All configuration is done through environment variables in the `.env` file:

- **Database Configuration**:
  - `DB_HOST`: Database host (default: localhost)
  - `DB_PORT`: Database port (default: 5432)
  - `DB_NAME`: Database name (default: heimdal_some_data)
  - `DB_USER`: Database user (default: postgres)
  - `DB_PASSWORD`: Database password

- **API Keys**:
  - `TWITTER_API_KEY`, `TWITTER_API_SECRET`, etc.: Twitter API credentials
  - `FACEBOOK_APP_ID`, `FACEBOOK_APP_SECRET`, etc.: Facebook API credentials
  - `TIKTOK_API_KEY`, `TIKTOK_API_SECRET`: TikTok API credentials
  - `SEO_API_KEY`: SEO API key (Ahrefs/Moz)
  - `OPENAI_API_KEY`: OpenAI API key (optional, for trend analysis)

- **API Configuration**:
  - `API_HOST`: Host to bind the API server to (default: 0.0.0.0)
  - `API_PORT`: Port to bind the API server to (default: 8000)

- **Data Collection Schedule**:
  - `DATA_COLLECTION_SCHEDULE`: Cron expression for the data collection schedule (default: "0 0 * * *", which is daily at midnight)

## Development

### Project Structure

```
heimdal_data/
├── api/                  # API endpoints
│   ├── __init__.py
│   ├── app.py            # FastAPI application
│   └── routes.py         # API routes
├── collectors/           # Data collectors
│   ├── __init__.py
│   ├── base_collector.py # Base collector class
│   ├── twitter_collector.py
│   ├── facebook_collector.py
│   ├── tiktok_collector.py
│   └── google_trends_collector.py
├── database/             # Database models and connection
│   ├── __init__.py
│   ├── database.py       # Database connection
│   └── models.py         # SQLAlchemy models
├── scripts/              # Utility scripts
│   ├── README.md         # Script documentation
│   └── setup_database.py # Database setup script
├── utils/                # Utility functions
├── config/               # Configuration files
├── logs/                 # Log files
├── __init__.py
├── main.py               # Entry point
├── requirements.txt      # Dependencies
└── .env.example          # Example environment variables
```

### Setting Up for Production

To set up the application for production:

1. Install the required dependencies:
   ```bash
   pip install -r heimdal_data/requirements.txt
   ```

2. Set up a PostgreSQL database using the provided script:
   ```bash
   cd heimdal_data
   ./scripts/setup_database.py --update-env
   ```
   
   This will create a PostgreSQL database and update the `.env` file with the connection details.

3. Obtain API keys for the social media platforms and update the `.env` file with the keys.

4. Start the application:
   ```bash
   python heimdal_data/main.py
   ```

### Testing the Application

The application includes a testing mode that uses SQLite instead of PostgreSQL and generates mock data. To enable testing mode:

1. Set `TESTING=true` in the `.env` file.
2. Start the application:
   ```bash
   python heimdal_data/main.py
   ```
3. Trigger a manual data collection:
   ```bash
   curl -X POST http://localhost:8000/api/data/fetch
   ```
4. Retrieve the collected data:
   ```bash
   curl -X GET http://localhost:8000/api/data/seo | python -m json.tool
   ```

### Adding a New Collector

To add a new data collector:

1. Create a new file in the `collectors` directory
2. Implement a class that inherits from `BaseCollector`
3. Implement the `collect` and `save` methods
4. Add the collector to the `__init__.py` file in the `collectors` directory
5. Update the `routes.py` file to use the new collector

## License

[MIT License](LICENSE)
