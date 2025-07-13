import pyttsx3

engine = pyttsx3.init()
engine.save_to_file("Hello, this is a test for OpenAI Whisper speech-to-text transcription. I need to get information about the real estate market, how many people live in the area, and what the average rent is.", 'sample.wav')
engine.runAndWait()

print("sample.wav generated.")