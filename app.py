from sentence_transformers import SentenceTransformer
import streamlit as st
from elasticsearch import Elasticsearch
from utils.rag import rag

es_client = Elasticsearch("http://127.0.0.1:9200")
embedding_model = SentenceTransformer("multi-qa-mpnet-base-cos-v1")


def print_log(message):
    print(message, flush=True)


def main():
    print_log("Starting the application...")
    st.title("The Tim Ferriss Show Archivist")

    user_input = st.text_input("Enter your input:")

    if st.button("Ask"):
        with st.spinner("Processing..."):
            output = rag(es_client, user_input)
            st.success("Completed!")
            st.write(output)


print_log("Streamlit app loop completed")

if __name__ == "__main__":
    print_log("Streamlit app started")
    main()
