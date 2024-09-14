from elasticsearch import Elasticsearch
from tqdm import tqdm
from utils.constants import INDEX_NAME


def ingest_documents(
    documents: list, es_url: str = "http://127.0.0.1:9200", index_name: str = INDEX_NAME
):
    es_client = Elasticsearch(es_url)
    index_settings = {
        "settings": {"number_of_shards": 1, "number_of_replicas": 0},
        "mappings": {
            "properties": {
                "id": {"type": "integer"},
                "title": {"type": "text"},
                "url": {"type": "keyword"},
                "chunk_id": {"type": "keyword"},
                "chunk": {"type": "text"},
                "embedding": {
                    "type": "dense_vector",
                    "dims": 768,
                    "index": True,
                    "similarity": "cosine",
                },
            }
        },
    }
    if not (es_client.indices.exists(INDEX_NAME)):
        es_client.indices.create(index=index_name, body=index_settings)
    for doc in tqdm(documents):
        es_client.index(index=index_name, document=doc)
