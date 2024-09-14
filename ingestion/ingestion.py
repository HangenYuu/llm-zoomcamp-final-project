from typing import Iterable
from elasticsearch import Elasticsearch
from tqdm import tqdm
from utils.constants import INDEX_NAME, DEFAULT_ES_SETTINGS


def ingest_documents(
    document: Iterable | dict,
    es_client: Elasticsearch,
    index_name: str = INDEX_NAME,
    index_settings: dict = DEFAULT_ES_SETTINGS,
):
    if not (es_client.indices.exists(index=INDEX_NAME)):
        es_client.indices.create(index=index_name, body=index_settings)

    if isinstance(document, dict):
        es_client.index(index=index_name, document=document)
        return

    for doc in tqdm(document):
        es_client.index(index=index_name, document=doc)
