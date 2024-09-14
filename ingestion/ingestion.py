from elasticsearch import Elasticsearch
from tqdm.auto import tqdm


def ingest_documents(documents: list, es_url: str = "http://127.0.0.1:9200"):
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
            }
        },
    }
    index_name = "tf_transcript"
    es_client.indices.create(index=index_name, body=index_settings)
    for doc in tqdm(documents):
        es_client.index(index=index_name, document=doc)
