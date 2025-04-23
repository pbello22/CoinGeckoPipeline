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
