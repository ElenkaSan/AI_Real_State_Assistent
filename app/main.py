from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import chat, speak, upload, reset, test_audio 


app = FastAPI(
    title="AI Real Estate Voice Assistant",
    description="A voice-enabled LLM assistant for exploring commercial listings.",
    version="0.1.0"
)

app.include_router(test_audio.router, prefix="/audio")

# this section for CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or ["http://localhost:3000"] for React
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Route registrations
app.include_router(chat.router, prefix="/chat")
app.include_router(speak.router, prefix="/speak")
app.include_router(upload.router, prefix="/upload_rag_docs")
app.include_router(reset.router, prefix="/reset")

@app.get("/")
def root():
    return {"message": "AI Real Estate Voice Assistant is running!"}

