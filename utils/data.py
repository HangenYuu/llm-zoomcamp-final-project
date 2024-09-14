import json
from pathlib import Path


def get_documents(filepath: Path | str) -> list:
    with open(filepath, "rt") as f_in:
        documents = json.load(f_in)
    return documents
