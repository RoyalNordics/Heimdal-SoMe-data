# Opgave:
Byg et dataindsamlingsmodul til Heimdal, der henter og lagrer data fra sociale medier, Google Trends og SEO-platforme. Modulet skal automatisk hente relevante oplysninger dagligt og gemme dem i en PostgreSQL-database.

## 📌 Funktioner i Dataindsamlingsmodulet

### 1️⃣ Datakilder & API'er
- Twitter API → Hent trending hashtags & engagement rates
- Facebook Graph API → Hent opslag, likes, kommentarer
- TikTok API → Hent populære hashtags og interaktionsdata
- Google Trends API → Hent søgeordsinteresse over tid
- Ahrefs/Moz API (valgfrit) → SEO-scorer for hashtags

### 2️⃣ Database (PostgreSQL)
- Tabel til hashtag-trends (hashtag, platform, engagement, timestamp)
- Tabel til SoMe-engagement (post-type, reach, likes, kommentarer, timestamp)
- Tabel til SEO-data (søgeord, trendscore, volumen, timestamp)

### 3️⃣ Automatisering
- Opsæt cron-job eller scheduled task, der kører scriptet hver dag
- Log alle hentede data i en fil/database for fejlsikring

### 4️⃣ API-Endpoints i FastAPI
- GET /api/data/trends → Returnerer seneste hashtag-trends
- GET /api/data/engagement → Returnerer engagement-statistik
- POST /api/data/fetch → Trigger en manuel dataindsamling

## 🛠 Teknisk Arkitektur

### Backend:
- Python (FastAPI) → API til dataindsamling og forespørgsler
- Requests & Tweepy → Hent data fra SoMe-API'er
- PyTrends → Hent data fra Google Trends
- Pandas & SQLAlchemy → Databehandling og databaseintegration

### Database: PostgreSQL
- Docker-container til PostgreSQL (valgfrit)
- Bruger SQLAlchemy ORM til forespørgsler

## 📌 Opgavedefinition til Cline

### Trin 1: Opsæt en PostgreSQL-database med tabellerne:
- ✅ hashtag_trends → platform, hashtag, engagement, timestamp
- ✅ social_engagement → platform, opslagstype, likes, kommentarer, reach
- ✅ seo_data → søgeord, trendscore, volumen, timestamp

### Trin 2: Implementér API-kald til Twitter API, Facebook API, Google Trends
- ✅ Hent trending hashtags fra Twitter
- ✅ Hent engagement-data fra Facebook & TikTok
- ✅ Hent søgetrends fra Google Trends

### Trin 3: Opret FastAPI-endpoints
- ✅ GET /api/data/trends → Returnerer seneste hashtag-trends
- ✅ GET /api/data/engagement → Returnerer engagement-data
- ✅ POST /api/data/fetch → Trigger en manuel dataindsamling

### Trin 4: Opsæt cron-job eller scheduled task
- ✅ Automatisér dataindsamling hver 24. time
- ✅ Log fejlhåndtering og API-responser

## ⚡ Output fra Cline
- 🔹 Python backend med API-kald til sociale medier
- 🔹 PostgreSQL-database med strukturerede tabeller
- 🔹 Automatiseret dataindsamling via cron-job
- 🔹 API-endpoints til at tilgå data

## Ekstra Info:
- Brug OpenAI API til at analysere trends, hvis muligt
- Gem API-nøgler i .env for sikkerhed
