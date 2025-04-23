import functions_framework
import requests
import pandas as pd
import json
import uuid
from datetime import datetime
from google.cloud import bigquery, storage

@functions_framework.http
def crypto_price_job(request):
    project_id = "portfolio-457020"
    bq_client = bigquery.Client(project=project_id)
    storage_client = storage.Client(project=project_id)

    # 1. Call CoinGecko API
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": "bitcoin,ethereum,beam,immutable",
        "vs_currencies": "usd"
    }
    response = requests.get(url, params=params)
    data = response.json()

    # 2. Format rows
    timestamp = datetime.utcnow()
    rows = [
        {"timestamp": timestamp, "coin": coin, "price_usd": price["usd"]}
        for coin, price in data.items()
    ]
    df = pd.DataFrame(rows)

    # 3. Save as JSONL to GCS
    bucket_name = "crypto-raw-data-portfolio-project"
    jsonl_filename = f"prices_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex}.jsonl"
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(jsonl_filename)
    json_lines = "\n".join([json.dumps(row, default=str) for row in rows]) 
    blob.upload_from_string(data=json_lines, content_type="application/json")

    # 4. Upload to BigQuery
    table_id = f"{project_id}.crypto_data.raw_crypto_prices"
    job = bq_client.load_table_from_dataframe(df, table_id)
    job.result()

    return "Daily crypto ETL complete", 200
