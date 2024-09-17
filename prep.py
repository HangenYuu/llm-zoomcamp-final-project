import os
from elasticsearch import Elasticsearch
from dotenv import load_dotenv

from db import init_db
from utils.constants import INDEX_NAME, DEFAULT_ES_SETTINGS
from huggingface_hub import hf_hub_download

load_dotenv()

ELASTIC_URL = os.getenv("ELASTIC_URL_LOCAL")


def download_huggingface_data():
    print("Downloading data from Hugging Face...")
    repo_id = "HangenYuu/tim-ferriss-transcript"
    filenames = [
        "chunked_embedded_data.json",
        "chunked_data.json",
        "ground-truth-retrieval.csv",
    ]
    local_dir = "data"

    for filename in filenames:
        hf_hub_download(
            repo_id=repo_id, filename=filename, repo_type="dataset", local_dir=local_dir
        )

    print("Data downloaded successfully")


def setup_elasticsearch():
    print("Setting up Elasticsearch...")
    es_client = Elasticsearch(ELASTIC_URL)

    if not es_client.indices.exists(index=INDEX_NAME):
        es_client.indices.create(index=INDEX_NAME, body=DEFAULT_ES_SETTINGS)
        print(f"Elasticsearch index '{INDEX_NAME}' created")
    else:
        print(f"Elasticsearch index '{INDEX_NAME}' already created")


def main():
    # you may consider to comment <start>
    # if you just want to init the db or didn't want to re-index
    print("Starting the indexing process...")

    download_huggingface_data()
    setup_elasticsearch()

    # you may consider to comment <end>

    print("Initializing database...")
    init_db()

    print("Indexing process completed successfully!")


if __name__ == "__main__":
    main()
