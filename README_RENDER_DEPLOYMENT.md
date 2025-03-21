# Deploying Heimdal SoMe Data to Render

This guide explains how to deploy the Heimdal SoMe Data API to [Render](https://render.com).

## Prerequisites

- A Render account
- Your code pushed to a GitHub or GitLab repository
- PostgreSQL database (you can use an existing one or create a new one on Render)

## Deployment Options

There are two ways to deploy to Render:

### Option 1: Use the Blueprint (render.yaml)

1. Log in to your Render dashboard.
2. Click "New" and select "Blueprint".
3. Connect your repository.
4. Render will detect the `render.yaml` file and configure your service.
5. Fill in the required environment variables.
6. Click "Apply" to deploy.

### Option 2: Manual Setup

1. Log in to your Render dashboard.
2. Click "New" and select "Web Service".
3. Connect your repository.
4. Configure your service:
   - **Name**: heimdal-some-data (or another name)
   - **Environment**: Python
   - **Region**: Choose a region close to your users
   - **Branch**: main (or your preferred branch)
   - **Build Command**: `pip install -r heimdal_data/requirements.txt`
   - **Start Command**: `cd heimdal_data && python main.py`
   - **Health Check Path**: `/health`

## Environment Variables

Set the following environment variables in your Render dashboard:

### Required Variables

- `TESTING`: Set to `false` for production
- `API_HOST`: Set to `0.0.0.0`
- `DB_HOST`: Your PostgreSQL host
- `DB_PORT`: PostgreSQL port (usually `5432`)
- `DB_NAME`: Your database name
- `DB_USER`: PostgreSQL username
- `DB_PASSWORD`: PostgreSQL password

### API Keys (as needed)

- `TWITTER_API_KEY`
- `TWITTER_API_SECRET`
- `TWITTER_ACCESS_TOKEN`
- `TWITTER_ACCESS_SECRET`
- `TWITTER_BEARER_TOKEN`
- `FACEBOOK_APP_ID`
- `FACEBOOK_APP_SECRET`
- `FACEBOOK_ACCESS_TOKEN`
- `TIKTOK_API_KEY`
- `TIKTOK_API_SECRET`
- `SEO_API_KEY`
- `OPENAI_API_KEY` (optional)

## OAuth Callback URLs

For Threads/Instagram API or any other OAuth service, use these URLs:

- Install Callback URL: `https://your-app-name.onrender.com/api/auth/callback`
- Uninstall Callback URL: `https://your-app-name.onrender.com/api/auth/uninstall`
- Data Deletion Callback URL: `https://your-app-name.onrender.com/api/auth/data-deletion`

## Verify Deployment

1. After deployment, visit `https://your-app-name.onrender.com/` to see the API welcome message.
2. Check the API documentation at `https://your-app-name.onrender.com/docs`.
3. Verify the health check endpoint at `https://your-app-name.onrender.com/health`.

## Troubleshooting

If you encounter issues:

1. Check the logs in your Render dashboard.
2. Verify all environment variables are set correctly.
3. Make sure your database is accessible from Render.
4. Check that the health check endpoint is returning `status: ok`.

## Local Testing

Before deploying, test your application locally:

```bash
# Set environment variables
export TESTING=false
export DB_HOST=your_db_host
# ... set other variables ...

# Run the application
python heimdal_data/main.py
```

Visit `http://localhost:8000/docs` to ensure everything works as expected.
