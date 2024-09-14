from groq import Groq
from dotenv import dotenv_values
from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer
from constants import INDEX_NAME, DEFAULT_MODEL

config = dotenv_values("../.env")
client = Groq(
    api_key=config["GROQ_API_KEY"],
)

model = SentenceTransformer("multi-qa-mpnet-base-cos-v1")


def elastic_keyword_search(
    es_client: Elasticsearch, query: str, index_name: str = INDEX_NAME
) -> list:
    search_query = {
        "size": 3,
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


def llm(prompt: str, model: str = DEFAULT_MODEL) -> str | None:
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model=model,
    )

    return chat_completion.choices[0].message.content


def build_prompt(query: str, search_results: list) -> str:
    context = ""

    for doc in search_results:
        context += f'section: {doc["section"]}\nquestion: {doc["question"]}\nanswer:: {doc["text"]}\n\n'

    prompt_template = """You're a course teaching assistant. You will answer QUESTION using information from CONTEXT only.

    QUESTION: {question}

    CONTEXT:
    {context}
    """
    prompt = prompt_template.format(question=query, context=context).strip()
    return prompt
