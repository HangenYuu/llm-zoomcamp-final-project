import os
import time
import json

from openai import OpenAI
from groq import Groq

from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer

from utils.rag import elastic_keyword_search, elastic_semantic_search, build_prompt

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "your-api-key-here")
ELASTIC_URL = os.getenv("ELASTIC_URL", "http://elasticsearch:9200")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-api-key-here")


es_client = Elasticsearch(ELASTIC_URL)
groq_client = Groq(api_key=GROQ_API_KEY)
openai_client = OpenAI(api_key=OPENAI_API_KEY)

model = SentenceTransformer("multi-qa-mpnet-base-cos-v1")


def llm(prompt: str, model_choice: str) -> tuple[str | None, dict[str, int], float]:
    start_time = time.time()
    if model_choice.startswith("groq/"):
        response = groq_client.chat.completions.create(
            model=model_choice.split("/")[-1],
            messages=[{"role": "user", "content": prompt}],
        )
        answer = response.choices[0].message.content
        tokens = {
            "prompt_tokens": response.usage.prompt_tokens,
            "completion_tokens": response.usage.completion_tokens,
            "total_tokens": response.usage.total_tokens,
        }
    elif model_choice.startswith("openai/"):
        response = openai_client.chat.completions.create(
            model=model_choice.split("/")[-1],
            messages=[{"role": "user", "content": prompt}],
        )
        answer = response.choices[0].message.content
        tokens = {
            "prompt_tokens": response.usage.prompt_tokens,
            "completion_tokens": response.usage.completion_tokens,
            "total_tokens": response.usage.total_tokens,
        }
    else:
        raise ValueError(f"Unknown model choice: {model_choice}")

    end_time = time.time()
    response_time = end_time - start_time

    return answer, tokens, response_time


def evaluate_relevance(question: str, answer: str):
    prompt_template = """
    You are an expert evaluator for a Retrieval-Augmented Generation (RAG) system.
    Your task is to analyze the relevance of the generated answer to the given question.
    Based on the relevance of the generated answer, you will classify it
    as "NON_RELEVANT", "PARTLY_RELEVANT", or "RELEVANT".

    Here is the data for evaluation:

    Question: {question}
    Generated Answer: {answer}

    Please analyze the content and context of the generated answer in relation to the question
    and provide your evaluation in parsable JSON without using code blocks:

    {{
      "Relevance": "NON_RELEVANT" | "PARTLY_RELEVANT" | "RELEVANT",
      "Explanation": "[Provide a brief explanation for your evaluation]"
    }}
    """.strip()

    prompt = prompt_template.format(question=question, answer=answer)
    evaluation, tokens, _ = llm(prompt, "groq/llama-guard-3-8b")

    try:
        json_eval = json.loads(evaluation)
        return json_eval["Relevance"], json_eval["Explanation"], tokens
    except json.JSONDecodeError:
        return "UNKNOWN", "Failed to parse evaluation", tokens


def calculate_token_cost(model_choice: str, tokens):
    token_cost = 0

    if model_choice in ["groq/llama-3.1-8b-instant", "groq/llama3-8b-8192"]:
        token_cost = (
            tokens["prompt_tokens"] * 0.05 + tokens["completion_tokens"] * 0.08
        ) / 1000000
    elif model_choice == "openai/gpt-4o":
        token_cost = (
            tokens["prompt_tokens"] * 5 + tokens["completion_tokens"] * 15
        ) / 1000000
    elif model_choice == "openai/gpt-4o-mini":
        token_cost = (
            tokens["prompt_tokens"] * 0.15 + tokens["completion_tokens"] * 0.6
        ) / 1000000

    return token_cost


def get_answer(query, model_choice, search_type):
    if search_type == "Vector":
        search_results = elastic_semantic_search(es_client, query, model)
    else:
        search_results = elastic_keyword_search(es_client, query)

    prompt = build_prompt(query, search_results)
    answer, tokens, response_time = llm(prompt, model_choice)

    relevance, explanation, eval_tokens = evaluate_relevance(query, answer)

    token_cost = calculate_token_cost(model_choice, tokens)

    return {
        "answer": answer,
        "response_time": response_time,
        "relevance": relevance,
        "relevance_explanation": explanation,
        "model_used": model_choice,
        "prompt_tokens": tokens["prompt_tokens"],
        "completion_tokens": tokens["completion_tokens"],
        "total_tokens": tokens["total_tokens"],
        "eval_prompt_tokens": eval_tokens["prompt_tokens"],
        "eval_completion_tokens": eval_tokens["completion_tokens"],
        "eval_total_tokens": eval_tokens["total_tokens"],
        "token_cost": token_cost,
    }
