__import__("pysqlite3")
import sys
sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")
import sqlite3

import streamlit as st
import os
from utils.layout import page_config
from utils.ai_inference import gpt4o_inference
from utils.chroma_db import initialise_persistent_chromadb_client_and_collection, add_document_chunk_to_chroma_collection, query_chromadb_collection

page_config()

def read_all_txt_files(directory):

    all_texts = {}

    for filename in os.listdir(directory):
        
        if filename.endswith(".txt"):
            
            file_path = os.path.join(directory, filename)
            
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                
                all_texts[filename] = content
    
    return all_texts

st.markdown("## Exercise 2.4 Creating a RAG Application with Chroma")

if "vdb_chunks" not in st.session_state:
    st.session_state.vdb_chunks = read_all_txt_files("document_chunks")

chroma_client = initialise_persistent_chromadb_client_and_collection("contract_supply_of_goods")

for file_name, chunk in st.session_state.vdb_chunks.items():

    add_document_chunk_to_chroma_collection(chroma_client, file_name, chunk)

st.markdown("Query")

query = st.text_area(
    "query",
    label_visibility="collapsed"
)

if st.button("Respond"):

    top_chunk = query_chromadb_collection(chroma_client, query, 1)
    
    st.markdown("#### Top Chunk")

    st.markdown(top_chunk)

    response = gpt4o_inference(
        "You are a lawyer who advises on contract interpretation.", 
        f"""
        Based on the following text extracted from the contract:
        <extracted text>
        {top_chunk}
        </extracted text>
        Answer the following question:
        <question>\
        {query}
        </question>
        Make sure to reference your answer according to the extracted text.
        """
    )

    st.markdown("#### Contractual Interpretation")

    st.markdown(response)