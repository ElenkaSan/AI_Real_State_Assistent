# from fastapi import APIRouter, UploadFile, File, HTTPException
# from pydub import AudioSegment
# import openai
# import io

# router = APIRouter()

# @router.post("/")
# async def transcribe_audio(audio: UploadFile = File(...)):
#     try:
#         # Convert audio to bytes
#         audio_bytes = await audio.read()
#         audio_file = io.BytesIO(audio_bytes)

#         # Send to Whisper API
#         transcript = openai.Audio.transcribe("whisper-1", audio_file)
#         return {"text": transcript['text']}

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

import openai
from openai import OpenAI
import os
from fastapi import UploadFile, File, APIRouter, HTTPException
import io

router = APIRouter()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@router.post("/")
async def transcribe_audio(audio: UploadFile = File(...)):
    try:
        audio_bytes = await audio.read()
        audio_file = io.BytesIO(audio_bytes)
        audio_file.name = "input.wav"  # Required for OpenAI API

        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )

        return {"text": transcript.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
