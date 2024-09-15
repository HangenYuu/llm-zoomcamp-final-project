# llm-zoomcamp-final-project
Final project for DataTalk.Club LLM Zoomcamp
Steps:
- [x] 1. Scrape the data.
- [x] 2. Chunk the data.
- [x] 3. Tokenize the data.
- [x] 4. Ingest the data into an ElasticSearch Docker
- [x] 5. Perform RAG trial with Groq API & Phi-3 (Ollama)
- [ ] 6. Build an UI for the app
- [ ] 7. Perform Evaluations with GPT-4o
- [ ] 8. Build a dashboard for evalution
- [ ] 9. Best practices: Hybrid search, Document re-ranking
- [ ] 10. Cloud deployment: HuggingFace Space (no monitoring)

# Points
Problem description
- [ ] 2 points: The problem is well-described and it's clear what problem the project solves

RAG flow
- [ ] 2 points: Both a knowledge base and an LLM are used in the RAG flow

Retrieval evaluation

    0 points: No evaluation of retrieval is provided
    1 point: Only one retrieval approach is evaluated
    2 points: Multiple retrieval approaches are evaluated, and the best one is used

RAG evaluation

    0 points: No evaluation of RAG is provided
    1 point: Only one RAG approach (e.g., one prompt) is evaluated
    2 points: Multiple RAG approaches are evaluated, and the best one is used

Interface
- [ ] 2 points: UI (e.g., Streamlit), web application (e.g., Django), or an API (e.g., built with FastAPI)

Ingestion pipeline
- [ ] 2 points: Automated ingestion with a Python script or a special tool (e.g., Mage, dlt, Airflow, Prefect)

Monitoring

    0 points: No monitoring
    1 point: User feedback is collected OR there's a monitoring dashboard
    2 points: User feedback is collected and there's a dashboard with at least 5 charts

Containerization

    0 points: No containerization
    1 point: Dockerfile is provided for the main application OR there's a docker-compose for the dependencies only
    2 points: Everything is in docker-compose

Reproducibility

    0 points: No instructions on how to run the code, the data is missing, or it's unclear how to access it
    1 point: Some instructions are provided but are incomplete, OR instructions are clear and complete, the code works, but the data is missing
    2 points: Instructions are clear, the dataset is accessible, it's easy to run the code, and it works. The versions for all dependencies are specified.

Best practices

    Hybrid search: combining both text and vector search (at least evaluating it) (1 point)