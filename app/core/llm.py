from app.core.memory import get_memory
import os
import time
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferWindowMemory
from app.core.rag import get_vector_store

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

def get_response_with_rag(user_id: str, message: str, chat_history: list):
    # memory = ConversationBufferWindowMemory(k=15, return_messages=True)

    llm = ChatOpenAI(
        temperature=0.2,
        model_name="gpt-4o",
        openai_api_key=openai_api_key
    )

    retriever = get_vector_store().as_retriever(
        search_type="mmr",
        search_kwargs={'k': 5, 'fetch_k': 20}
    )

    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        # memory=memory,
        return_source_documents=True
    )

    start = time.time()
    response = chain.invoke({
        "question": message,
        "chat_history": chat_history
    })
    duration = int((time.time() - start) * 1000)

    print("\n" + "="*50)
    print("            RAG RETRIEVAL RESULTS            ")
    print("="*50)
    source_documents = response.get('source_documents', [])
    if source_documents:
        print(f"Found {len(source_documents)} matching document(s):")
        for i, doc in enumerate(source_documents):
            row_number = doc.metadata.get('row', 'N/A')
            print(f"\n--- Match {i+1} (Source Row: {row_number}) ---")
            print(doc.page_content)
    else:
        print("No documents found by the retriever.")
    print("="*50 + "\n")

    return response["answer"], duration
