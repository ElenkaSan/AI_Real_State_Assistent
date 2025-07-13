import requests
import os
import shutil

# The base URL of your running FastAPI application
BASE_URL = "http://127.0.0.1:8000"

# The path to your CSV file. Make sure this path is correct.
# You might need to create this file or use an existing one.
CSV_FILE_PATH = os.path.join("data", "HackathonInternalKnowledgeBase.csv")

def test_upload():
    """Tests the /upload_rag_docs endpoint."""
    print("--- Testing File Upload ---")
    url = f"{BASE_URL}/upload_rag_docs"
    
    # Check if the file exists before trying to upload
    if not os.path.exists(CSV_FILE_PATH):
        print(f"Error: The file '{CSV_FILE_PATH}' was not found.")
        print("Please make sure you have a CSV file at that location.")
        return

    with open(CSV_FILE_PATH, 'rb') as f:
        files = {'file': (os.path.basename(CSV_FILE_PATH), f, 'text/csv')}
        try:
            response = requests.post(url, files=files)
            # Raise an exception if the request was unsuccessful
            response.raise_for_status()
            print("Upload successful!")
            print("Server response:", response.json())
        except requests.exceptions.RequestException as e:
            print(f"An error occurred during upload: {e}")
    print("---------------------------\n")

def start_interactive_chat():
    """Starts an interactive chat session with the user."""
    print("--- Starting Interactive Chat Session ---")
    print("Type 'quit' or 'exit' to end the conversation.")
    
    # This list will store the conversation history
    chat_history = []
    user_id = "interactive-user-123"
    url = f"{BASE_URL}/chat"

    while True:
        try:
            user_message = input("You: ")
            if user_message.lower() in ["quit", "exit"]:
                print("Exiting chat. Goodbye!")
                break

            payload = {
                "user_id": user_id,
                "message": user_message,
                "chat_history": chat_history
            }

            response = requests.post(url, json=payload)
            response.raise_for_status()
            
            response_data = response.json()
            ai_response = response_data.get('response', 'Sorry, I did not get a valid response.')

            print(f"AI: {ai_response}")

            # Update the history with the latest exchange
            chat_history.append([user_message, ai_response])

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            break
        except KeyboardInterrupt:
            print("\nExiting chat. Goodbye!")
            break

if __name__ == "__main__":
    # Delete the existing ChromaDB vector store directory
    shutil.rmtree('./chroma_store', ignore_errors=True)

    # We still need to make sure the document is uploaded for the chat to work.
    # You only need to run this once per server restart.
    test_upload()

    # Start the continuous chat
    start_interactive_chat()