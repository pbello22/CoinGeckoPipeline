import requests
import pandas as pd
import json
import uuid
from datetime import datetime
from google.cloud import bigquery, storage
from google.oauth2 import service_account

# Authenticate with service account
credentials = service_account.Credentials.from_service_account_file("service_account.json")
project_id = credentials.project_id
bq_client = bigquery.Client(credentials=credentials, project=project_id)
storage_client = storage.Client(credentials=credentials, project=project_id)

# CoinGecko API request
url = "https://api.coingecko.com/api/v3/simple/price"
params = {
    "ids": "bitcoin,ethereum,beam,immutable",
    "vs_currencies": "usd"
}
response = requests.get(url, params=params)
data = response.json()

# Format API data into rows
timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
rows = [
    {"timestamp": timestamp, "coin": coin, "price_usd": price["usd"]}
    for coin, price in data.items()
]
df = pd.DataFrame(rows)

# Save data as newline-delimited JSON (JSONL) to GCS
bucket_name = "crypto-raw-data-portfolio-project"  # <-- update if needed
jsonl_filename = f"prices_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex}.jsonl"
bucket = storage_client.bucket(bucket_name)
jsonl_blob = bucket.blob(jsonl_filename)

# Create newline-delimited JSON string
json_lines = "\n".join([json.dumps(row) for row in rows])

# Upload to GCS
jsonl_blob.upload_from_string(
    data=json_lines,
    content_type="application/json"
)
print(f"JSONL saved to GCS as: {jsonl_filename}")

# Upload same data to BigQuery
table_id = f"{project_id}.crypto_data.prices"
job = bq_client.load_table_from_dataframe(df, table_id)
job.result()

print("Uploaded crypto prices to BigQuery!")
