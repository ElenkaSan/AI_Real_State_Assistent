import os
import time
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from app.core.rag import get_vector_store

# New imports for the advanced RAG chain
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

def get_response_with_rag(user_id: str, message: str, chat_history: list):
    llm = ChatOpenAI(
        temperature=0.2,
        model_name="gpt-4o",
        openai_api_key=openai_api_key
    )

    # 1. Reconfigure the Base Retriever for more results
    retriever = get_vector_store().as_retriever(
        search_type="mmr",
        search_kwargs={'k': 12, 'fetch_k': 50} # Increased k to 12
    )

    # 2. Create the History-Aware Retriever (Query Transformation)
    contextualize_q_system_prompt = (
        "Given a chat history and the latest user question "
        "which might reference context in the chat history, "
        "formulate a standalone question which can be understood "
        "without the chat history. Do NOT answer the question, "
        "just reformulate it if needed and otherwise return it as is."
    )
    contextualize_q_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", contextualize_q_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )
    history_aware_retriever = create_history_aware_retriever(
        llm, retriever, contextualize_q_prompt
    )

    # 3. Create the final Answer-Generation chain
    qa_system_prompt = (
        "You are an assistant for question-answering tasks. "
        "Use the following pieces of retrieved context to answer "
        "the question. If you don't know the answer, just say "
        "that you don't know. Keep the answer concise and directly based on the provided information."
        "\n\n"
        "{context}"
    )
    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", qa_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )
    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

    # 4. Combine everything into the final retrieval chain
    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

    # --- Invocation --- #
    start = time.time()
    
    # Invoke the new chain with the correct input structure
    response = rag_chain.invoke({"input": message, "chat_history": chat_history})
    
    duration = int((time.time() - start) * 1000)

    # The response structure is now different, we get the answer from 'answer' key
    # We no longer print the retrieval results here as the process is more complex,
    # but the improved accuracy should be evident in the final answer.

    return response.get("answer", "I'm sorry, I couldn't find an answer."), duration
