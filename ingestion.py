from pathlib import Path
from elasticsearch import Elasticsearch
from tqdm import tqdm
import ijson
from argparse import ArgumentParser

from utils.data import ingest_documents
from utils.constants import INDEX_NAME, DEFAULT_ES_SETTINGS


def main():
    parser = ArgumentParser()
    parser.add_argument("-p", "--path", default="data/chunked_embedded_data.json")

    args = parser.parse_args()
    filepath = Path(args.path)

    es_client = Elasticsearch("http://127.0.0.1:9200")

    with open(filepath, "rt") as f:
        for item in tqdm(ijson.items(f, "item")):
            ingest_documents(item, es_client, INDEX_NAME, DEFAULT_ES_SETTINGS)


if __name__ == "__main__":
    main()
