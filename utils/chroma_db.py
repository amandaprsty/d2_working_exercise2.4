import chromadb
import chromadb.utils.embedding_functions as embedding_functions
import uuid
import os
from dotenv import load_dotenv

load_dotenv()

def initialise_persistent_chromadb_client_and_collection(collection_name):

    chroma_client = chromadb.PersistentClient(f"./data/chromadb/{collection_name}")

    collection = chroma_client.create_collection(
        name=collection_name,
        embedding_function=embedding_functions.OpenAIEmbeddingFunction(
            api_key=os.environ.get("OPENAI_API_KEY"),
            model_name="text-embedding-3-large"
        ),
        metadata={"hnsw:space": "cosine"},
        get_or_create=True
    )

    return collection

def add_document_chunk_to_chroma_collection(collection, document_name, document_chunk, document_id=None):

    if document_id is None:
        guid = uuid.uuid4()
        guid_string = str(guid)
        document_id = guid_string

    collection.add(
        documents=[document_chunk],
        metadatas=[{"document_name": document_name}],
        ids=[document_id]
    )

def query_chromadb_collection(collection, query, n_results):

    documents = collection.query(
        query_texts=[query],
        include=["documents", "metadatas"],
        n_results=n_results
    )

    return documents