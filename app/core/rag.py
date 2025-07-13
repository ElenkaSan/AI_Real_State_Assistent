from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
import csv
from langchain.docstore.document import Document
import os

CHROMA_PATH = "chroma_store"

def get_vector_store():
    return Chroma(persist_directory=CHROMA_PATH, embedding_function=OpenAIEmbeddings())

def save_and_index_csv(file_path: str):
    documents = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        # Use DictReader to easily access columns by their header name
        csv_reader = csv.DictReader(file)
        for row_num, row in enumerate(csv_reader):
            # Create the specific, distinct content for the vector search
            page_content = f"Listing at {row.get('Property Address', '')}, Floor {row.get('Floor', '')}, Suite {row.get('Suite', '')}"
            
            # The metadata will contain the full data of the row for the LLM to use
            # We also add the original row number for easy reference
            metadata = row
            metadata['source_row'] = row_num + 1 # Add 1 for header, 1 for 0-index

            documents.append(Document(page_content=page_content, metadata=metadata))

    db = Chroma.from_documents(documents, OpenAIEmbeddings(), persist_directory=CHROMA_PATH)
    db.persist()