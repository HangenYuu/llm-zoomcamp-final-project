import streamlit as st
from elasticsearch import Elasticsearch
from openai import OpenAI
from utils.rag import rag

es_client = Elasticsearch("http://127.0.0.1:9200")


def main():
    st.title("The Tim Ferriss Transcript Chat")

    user_input = st.text_input("Enter your input:")

    if st.button("Ask"):
        with st.spinner("Processing..."):
            output = rag(es_client, user_input)
            st.success("Completed!")
            st.write(output)


if __name__ == "__main__":
    main()
