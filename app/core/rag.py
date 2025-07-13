from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.document_loaders import CSVLoader
import os

CHROMA_PATH = "./chroma_store"

def get_vector_store():
    return Chroma(persist_directory=CHROMA_PATH, embedding_function=OpenAIEmbeddings())

def save_and_index_csv(file_path):
    loader = CSVLoader(file_path=file_path)
    documents = loader.load()
    db = Chroma.from_documents(documents, OpenAIEmbeddings(), persist_directory=CHROMA_PATH)
    db.persist()