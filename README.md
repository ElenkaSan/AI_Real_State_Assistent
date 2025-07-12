# AI Real Estate Assistant & CRM for Commercial Listings

An intelligent voice-based AI assistant + CRM that helps brokers and clients explore, analyze, and manage commercial real estate listings via natural conversation.

Voice Assistant → Whisper Speech-to-Text → GPT-4o (with LangChain + RAG over CSV) → Response  
Includes short-term memory (10–15 messages) and lightweight CRM (user name, email, history).


### Project Built by 

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

User speaks → voice is transcribed to text
Text is passed to `/chat` endpoint
LangChain keeps a window of the last 10–15 messages in memory
Query is combined with CSV content via RAG
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
│   │   └── reset.py            # /reset: Clear memory
│   ├── core/
│   │   ├── llm.py              # GPT-4o config & memory setup
│   │   ├── rag.py              # RAG (Chroma + CSV loader)
│   │   └── memory.py           # ConversationBufferWindowMemory config
│   └── models/
│       └── schema.py           # Request/Response Pydantic schemas
│
├── data/
│   └── listings.csv            # Real estate data source
│
├── frontend/ 
│   └── react-client/           # Chat UI (React + Mic Input) with voice + chat
│
├── docs/
│   ├── api_contracts.pdf       # Sample input/output formats, usage schema
│   ├── architecture.mmd        # Mermaid architecture diagram
│   └── conversation_sample.json
│
├── .env                        # API keys (placeholder)
├── requirements.txt            # Python dependencies
├── README.md                   
└── run.sh                      # Script to launch API locally
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

# 3. Add .env file with OpenAI API key
touch .env
# Add keys like:
# OPENAI_API_KEY=your-key
# WHISPER_API_KEY=your-key

# 4. Start the server
uvicorn app.main:app --reload
```

### Sample API Calls

POST /upload_rag_docs
Upload CSV to ChromaDB.

```
curl -X POST http://localhost:8000/upload_rag_docs \
  -F "file=@data/listings.csv"
```

POST /chat
Send a text query.

```
{
  "user_id": "abc123",
  "message": "What properties on 36th St have rent below $90?"
}
```
Returns:

```
{
  "response": "36 W 36th St, Suite 300, has $87.00/SF annual rent...",
  "duration_ms": 2134
}
```

POST /speak
Send voice → get transcript + AI reply.

```
curl -X POST http://localhost:8000/speak \
  -F "audio=@sample.wav"
```


### .env Format
env
```
OPENAI_API_KEY=your-openai-key
WHISPER_API_KEY=your-whisper-key
```

### What’s Next
Add optional TTS response using ElevenLabs or Edge API

Expand memory to Redis for longer sessions

Style UI with floating avatars and property cards

Built For
Okada&Co Hackaton
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

