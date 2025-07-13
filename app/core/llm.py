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

    retriever = get_vector_store().as_retriever()

    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        # memory=memory,
        return_source_documents=False
    )

    start = time.time()
    response = chain.invoke({
        "question": message,
        "chat_history": chat_history
    })
    duration = int((time.time() - start) * 1000)

    return response["answer"], duration
