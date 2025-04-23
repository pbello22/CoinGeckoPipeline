# Crypto Price ETL with Google Cloud Functions

A serverless Python function that fetches real-time cryptocurrency prices from the CoinGecko API, stores them in Google Cloud Storage as JSONL, and loads them into BigQuery for analysis.

This project includes:
- An **automated ETL script** (Google Cloud Function version)
- A **manual script** for local execution using a service account

## Tech Stack
- Google Cloud Functions
- BigQuery
- Cloud Storage
- Python + Pandas
- CoinGecko API (no API key required)

## Setup Instructions

1. Replace `"insert_project_here"` in `crypto_price_job()` with your actual GCP project ID, or set it as an environment variable in deployment.
2. Deploy the function using the `gcloud` CLI:
   ```bash
   gcloud functions deploy crypto_price_job \
     --runtime python310 \
     --trigger-http \
     --allow-unauthenticated \
     --project YOUR_PROJECT_ID \
     --entry-point crypto_price_job
