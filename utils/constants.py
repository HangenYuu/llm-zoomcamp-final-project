INDEX_NAME = "tf_transcript"
DEFAULT_MODEL = "llama3-8b-8192"
DEFAULT_ES_SETTINGS = {
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
