import os
import io
import requests
import subprocess
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
router = APIRouter()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

CONVERTED_PATH = "data/output.wav"


@router.get("/test-audio")
async def get_test_audio():
    """Returns a pre-saved audio file"""
    if not os.path.exists(CONVERTED_PATH):
        raise HTTPException(status_code=404, detail="No test audio found.")
    return FileResponse(CONVERTED_PATH, media_type="audio/wav")

@router.post("/speak-test")
async def speak_from_local():
    """Transcribes local bundled test audio"""
    try:
        if not os.path.exists(CONVERTED_PATH):
            raise Exception("Local test audio not found. Please run the generator script.")

        with open(CONVERTED_PATH, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )

        return {"text": transcription.text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


