from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.document_loaders.csv_loader import CSVLoader
import os

CHROMA_PATH = "./chroma_store"

def get_vector_store():
    return Chroma(persist_directory=CHROMA_PATH, embedding_function=OpenAIEmbeddings())

def save_and_index_csv(file_path):
    loader = CSVLoader(file_path=file_path)
    documents = loader.load()
    db = Chroma.from_documents(documents, OpenAIEmbeddings(), persist_directory=CHROMA_PATH)
    db.persist()