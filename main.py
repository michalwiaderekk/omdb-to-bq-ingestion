import functions_framework
import requests
import json
from google.cloud import bigquery, storage
from datetime import datetime
import os

API_KEY = os.environ.get('API_KEY')  # request_json['api_key']
PROJECT_ID = os.environ.get('PROJECT_ID') 
DATASET_ID = os.environ.get('DATASET_ID') 
TABLE_ID = os.environ.get('TABLE_ID') 
BASE_URL = 'http://www.omdbapi.com/'

@functions_framework.http
def ingest_omdb_film(request):
    request_json = request.get_json(silent=True)
    title = request_json['title']

    bq_client = bigquery.Client(project=PROJECT_ID)

    print(f"Processing: {title}")
    params = {
        't': title,
        'apikey': API_KEY
    }
    try:
        response = requests.get(BASE_URL, params=params, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('Response') == 'True':
                bq_client.insert_rows_json(f'{DATASET_ID}.{TABLE_ID}',[data])
    except Exception as e:
        print(f"Error for title '{title}': {e}")

    return 'Success!'