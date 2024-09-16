# The Tim Ferriss Show Archivist

**The Tim Ferriss Show (TFS)** is one of the most popular podcast, focusing on "deconstructing world-class performers from eclectic areas (investing, chess, pro sports, etc.), digging deep to find the tools, tactics, and tricks that listeners can use". After 10 years and over 750 episodes, the content has grown to be intimidating to read and search for the gems.

**The TFS Archivist** is a conversational AI that can help users search for the relevant idea from a specific guest/episode, saving the need of manually skimming through the library and the hour-long transcript.

This is my final project for DataTalk.Club's [LLM Zoomcamp](https://github.com/DataTalksClub/llm-zoomcamp) - a free course about LLMs and RAG.

- [The Tim Ferriss Show Archivist](#the-tim-ferriss-show-archivist)
- [Progress](#progress)
- [Points](#points)
- [Overview](#overview)
- [Dataset](#dataset)
- [App Architecture](#app-architecture)
- [How to Run the App](#how-to-run-the-app)
  - [Docker Compose](#docker-compose)
  - [Development](#development)
- [Development Details](#development-details)
- [FAQs](#faqs)

# Progress

- [x] Scrape the data.
- [x] Chunk the data.
- [x] Tokenize the data.
- [x] Ingest the data into an ElasticSearch Docker
- [x] Perform RAG trial with Groq API & Phi-3 (Ollama)
- [x] Build an UI for the app
- [x] Perform Evaluations with GPT-4o
- [ ] Build a dashboard for evalution
- [ ] Best practices

# Points

To save you the trouble of looking for the project criteria, I put my marks here. You can double-check while reading through the repo and running it.

Problem description

- [x] 2 points: The problem is well-described and it's clear what problem the project solves

RAG flow

- [x] 2 points: Both a knowledge base and an LLM are used in the RAG flow

Retrieval evaluation

- [x] 2 points: Multiple retrieval approaches are evaluated, and the best one is used

RAG evaluation

- [x] 2 points: Multiple RAG approaches are evaluated, and the best one is used

Interface

- [x] 2 points: **UI (e.g., Streamlit)**, web application (e.g., Django), or an API (e.g., built with FastAPI)

Ingestion pipeline

- [x] 2 points: Automated ingestion with **a Python script** or a special tool (e.g., Mage, dlt, Airflow, Prefect)

Monitoring

- [ ] 2 points: User feedback is collected and there's a dashboard with at least 5 charts

      Grafana dashboard

Containerization

- [ ] 2 points: Everything is in docker-compose

Reproducibility

- [ ] 2 points: Instructions are clear, the dataset is accessible, it's easy to run the code, and it works. The versions for all dependencies are specified.

Best practices

- [ ] Hybrid search: combining both text and vector search (**at least evaluating it**) (1 point)
- [ ] Document re-ranking (1 point)
- [ ] User query rewriting (1 point)

# Overview

The TFS Archivist lets user search for a specific content from an episode of The Tim Ferriss Show.

Example use case incluces

1. Search for background information about a guest.
2. Search for the episode a guest appears in.
3. Search for a specific idea that a guest mentioned in the show.

# Dataset



# App Architecture

![architecture](assets/RAG_Workflow.excalidraw.png)

# How to Run the App
## Docker Compose

## Development
The app was created using GitHub Codespace, which is basically a Python environment on a Linux machine. Hence, it was the easiest to run using a (virtual) Linux machine, Ubuntu in particular.

1. Create a new virtual environment. For example, using conda

```bash
conda create -n llm
conda activate llm
# (Optional) Install uv for faster package installation
pip install uv
```

2. Install dependencies (`uv` is optional)

```bash
uv pip install torch --index-url https://download.pytorch.org/whl/cpu
uv pip install -r requirements.txt
```

3. Download data from HuggingFace by running the script in `data` folder

```bash
bash data/download.sh
```

4. Started the app with Docker Compose

```bash
docker-compose up
```

5. **After ElasticSearch container is initialized**, ingest the data in by running script in the `ingestion` folder.

```bash
python ingestion/ingestion.py
```

6. **After the data are fully ingested**, you can start using the app via the Streamlit UI.

# Development Details

# FAQs