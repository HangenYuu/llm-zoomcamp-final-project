from typing import Iterable
from elasticsearch import Elasticsearch
from tqdm import tqdm


def ingest_documents(
    document: Iterable | dict,
    es_client: Elasticsearch,
    index_name: str,
    index_settings: dict,
):
    if not (es_client.indices.exists(index=index_name)):
        es_client.indices.create(index=index_name, body=index_settings)

    if isinstance(document, dict):
        es_client.index(index=index_name, document=document)
        return

    for doc in tqdm(document):
        es_client.index(index=index_name, document=doc)
