import streamlit as st
import os
from utils.layout import page_config

page_config()

st.markdown("## Exercise 2.1 Chunking Documents")

def chunk_text(text, chunk_size=250):
    words = text.split()
    return [' '.join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]

def save_chunks(chunks, base_filename='chunk'):
    os.makedirs('document_chunks', exist_ok=True)
    for i, chunk in enumerate(chunks):
        filename = os.path.join('document_chunks', f'{base_filename}_{i+1}.txt')
        with open(filename, 'w') as file:
            file.write(chunk)

def read_first_file(directory='document_chunks'):
    
    files = sorted([f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))])
    
    if not files:
        raise FileNotFoundError("No files found in the directory.")
    
    first_file_path = os.path.join(directory, files[0])
    with open(first_file_path, 'r') as file:
        text = file.read()
    
    return text

uploaded_file = st.file_uploader(
    "document_upload", 
    type=["txt", "docx"],
    label_visibility="collapsed"
)

if uploaded_file is not None:
    
    file_content = uploaded_file.read().decode("utf-8")
    st.write("Document uploaded successfully.")

    chunks = chunk_text(file_content, chunk_size=250)
    st.write(f"Document has been chunked into {len(chunks)} sections.")

    save_chunks(chunks, base_filename=uploaded_file.name.split('.')[0])
    st.write(f"Chunks have been saved to the local directory under the 'document_chunks' folder.")

if st.button("Display First Chunk"):

    first_chunk = read_first_file()

    st.markdown(first_chunk)
    