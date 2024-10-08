from typing import Literal
from groq import Groq
from dotenv import dotenv_values
from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer
from .constants import INDEX_NAME, DEFAULT_MODEL
import os

env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.env"))
config = dotenv_values(env_path)
os.environ["HF_HOME"] = "/tmp"

client = Groq(
    api_key=config["GROQ_API_KEY"],
)


def elastic_keyword_search(
    es_client: Elasticsearch, query: str, index_name: str = INDEX_NAME
) -> list:
    search_query = {
        "size": 5,
        "query": {
            "bool": {
                "must": {
                    "multi_match": {
                        "query": query,
                        "fields": ["chunk", "title"],
                        "type": "best_fields",
                    }
                },
            }
        },
    }
    response = es_client.search(index=index_name, body=search_query)
    result_docs = []

    for hit in response["hits"]["hits"]:
        result_docs.append(hit["_source"])
    return result_docs


def elastic_semantic_search(
    es_client: Elasticsearch,
    query: str,
    model: SentenceTransformer,
    index_name: str = INDEX_NAME,
) -> list:
    vector_query = model.encode(query)
    knn_query = {
        "field": "embedding",
        "query_vector": vector_query,
        "k": 5,
        "num_candidates": 10000,
    }
    response = es_client.search(index=index_name, knn=knn_query)
    result_docs = []

    for hit in response["hits"]["hits"]:
        result_docs.append(hit["_source"])
    return result_docs


def llm(prompt: str, model: str = DEFAULT_MODEL) -> str | None:
    chat_completion = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    return chat_completion.choices[0].message.content


def build_prompt(query: str, search_results: list) -> str:
    context = ""

    for doc in search_results:
        context += f'episode title: {doc["title"]}\nepisode id: {doc["id"]}\ntranscript excerpt: {doc["chunk"]}\n\n'

    prompt_template = """You're a helpful archivist in charge of managing the transcripts of the podcast The Tim Ferriss Show. You help users answer their question based on the show transcript. You will answer QUESTION using information from CONTEXT only.
QUESTION: {question}

CONTEXT:
{context}"""

    prompt = prompt_template.format(question=query, context=context).strip()
    return prompt


def rag(
    es_client: Elasticsearch,
    query: str,
    model: str = DEFAULT_MODEL,
    embedding_model: SentenceTransformer | None = None,
    search_type: Literal["keyword", "semantic"] = "keyword",
) -> str | None:
    if search_type == "keyword":
        search_results = elastic_keyword_search(es_client, query)
    elif search_type == "semantic":
        search_results = elastic_semantic_search(es_client, query, embedding_model)

    prompt = build_prompt(query, search_results)
    return llm(prompt, model)
