# AI Real Estate Assistant & CRM for Commercial Listings

Voice Conversational Agentic AI:
An intelligent voice-based AI assistant + CRM that helps brokers and clients explore, analyze, and manage commercial real estate listings via natural conversation.

Voice Assistant → Whisper Speech-to-Text → GPT-4o (with LangChain + RAG over CSV) → Response  
Includes short-term memory (10–15 messages) and lightweight CRM (user name, email, history).


### Project Built by
[Elena Nurullina](https://www.linkedin.com/in/elena-nurullina) 

[Younes Slaoui](https://www.linkedin.com/in/younesslaoui)

![ai01](https://github.com/user-attachments/assets/90d29925-2523-4279-8952-42cc578730c1)

![ai02](https://github.com/user-attachments/assets/3cbbfb8d-3f8e-40b0-9c35-e6889d08c891)

### Work Plan – 2 Day Delivery

**Day 1:**
- Set up FastAPI with `/speak` + `/chat` endpoints
- Load CSV into ChromaDB + connect LangChain RAG

**Day 2:**
- Build React UI with mic input and chat bubbles
- Add LangChain memory buffer, test, and polish UI
- Finalize README, API contracts, and architecture diagram

### Technologies Used

```
| Layer            | Stack / Tools                              |
|------------------|--------------------------------------------|
| Backend          | FastAPI + LangChain                        |
| Speech-to-Text   | OpenAI Whisper API                         |
| LLM              | OpenAI GPT-4o                              |
| Memory           | LangChain `ConversationBufferWindowMemory` |
| RAG Store        | ChromaDB + CSV files                       |
| Frontend         | React + Tailwind/Bootstrap + `react-mic`   |
| CRM              | SQLite (lightweight, optional)             |
| Response Display:| Chat UI or Optional TTS Output             |

```

### Data Flow

User speaks → voice is transcribed to text is passed `/speak` and test audio is passed `/audio/test-audio`
Text is passed to `/chat` endpoint
LangChain keeps a window of the last 10–15 messages in memory
Query is combined with CSV content via RAG is passed `/upload_rag_docs`
OpenAI GPT-4o generates a contextual reply
Response is sent back to the frontend and optionally synthesized with TTS

### Structure

```
voice-agent-ai/
├── app/
│   ├── main.py                 # FastAPI entrypoint
│   ├── api/
│   │   ├── speak.py            # /speak: Voice to text (Whisper)
│   │   ├── chat.py             # /chat: Text input → LLM + RAG
│   │   ├── upload.py           # /upload_rag_docs: CSV ingestion
│   │   ├── reset.py            # /reset: Clear memory
│   │   └── test_audio.py            
│   ├── core/
│   │   ├── llm.py              # GPT-4o config & memory setup
│   │   ├── rag.py              # RAG (Chroma + CSV loader)
│   │   └── memory.py           # ConversationBufferWindowMemory config
│   └── models/
│       └── schema.py           # Request/Response Pydantic schemas
│
├── data/
│   ├── HackathonInternalKnowledgeBase.csv   # Real estate data source
│   ├── generate_long_sample.py  
│   └── output.wav                           # Voice test sample
|
├── docs/
│   ├── api_contracts.pdf       # Sample input/output formats, usage schema
│   ├── architecture.mmd        # Mermaid architecture diagram
│   └── conversation_sample.json
│
├── .env                        # API keys (placeholder)
├── requirements.txt            # Python dependencies
├── README.md                   
|── run.sh                      # Script to launch API locally
│
|   frontend/                   # Chat UI (React + Mic Input) with voice + chat
└── react-client/
    ├── public/
    │   ├── logo.png
    │   └── index.html
    ├── src/
    │   ├── App.js
    │   ├── index.js
    │   ├── assets/
    │   │   └── nyc-bg.jpg
    │   ├── components/
    │   │   ├── ChatWindow.js
    │   │   ├── MicInput.js
    │   │   ├── MicRecorder.js
    │   │   ├── MessageBubble.js
    │   │   └── Header.js
    ├── .env.local
    └── package.json

```

## Installation & Running Locally

```
# 1. Clone the repo
git clone https://github.com/yourteam/voice-agent-ai.git
cd voice-agent-ai

# 2. Create virtual env & install deps
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

Give run.sh permission:
chmod +x run.sh
./run.sh

# 3. Add .env file with OpenAI API key
touch .env
# Add keys like:
# OPENAI_API_KEY=your-key

# 4. Start the server
uvicorn app.main:app --reload

# 5. Open another terminal to run client side
cd frontend/rect-client 
npm install
npm start

```

### Sample API Calls

POST /upload_rag_docs
Upload CSV to ChromaDB.

```
curl --location 'http://localhost:8000/upload_rag_docs' \
--form 'file=@"/data/HackathonInternalKnowledgeBase.csv"'
```

Returns:

```
{
    "message": "File uploaded and indexed successfully"
}
```

POST /chat
Send a text query.

```
curl --location 'http://localhost:8000/chat' \
--header 'Content-Type: application/json' \
--data '{
    "user_id": "test123",
    "message": "Which suites have rent below $90?",
    "chat_history": []
}'
```
Returns:

```
{
    "response": "Based on the provided context, there are no suites with rent below $90 per square foot per year. The suite mentioned, Suite 903 at 104-110 E 40th St, has a rent of $95.00 per square foot per year.",
    "duration_ms": 2008
}
```

POST /speak
Send voice → get transcript + AI reply.

```
curl --location 'http://localhost:8000/speak' \
--form 'audio=@"/data/output.wav"'
```
Returns:

```
{"text":"Hello, this is a test for OpenAI Whisper Speech 2x transcription. I need to get information about the real estate market, how many people live in the area, and what the average rent is."}
```

GET /audio/test-audio

```
curl --location 'http://localhost:8000/audio/test-audio'
```
Returns audio format to listen.


### .env Format
env
```
OPENAI_API_KEY=your-openai-key
```

### What’s Next
Add optional TTS response using ElevenLabs or Edge API

Expand memory to Redis for longer sessions

Style UI with floating avatars and property cards

#### Built For Okada&Co Hackaton
Challenge Track: AI Voice Agent + CRM
July 2025

### Contributing
Open to PRs, issues, and feedback!

### Summary of Improvements

```
|---------------------|--------------------------------------------------------|
| Title               | More descriptive and eye-catching                      |
| Work Plan           | Bullet list format, visually scannable                 |
| Technologies        | Clean table with tools                                 |
| Data Flow           | Markdown-friendly list                                 |
| Folder Tree         | Clean code-style formatting                            |
| Setup               | Shell instructions with key reminders                  |
| Sample API          | Ready to test with cURL or Postman                     |
| .env Format         | Explicit format shown                                  |
| Professional polish | Emojis, headings, formatting -good hackathon impression|
```

