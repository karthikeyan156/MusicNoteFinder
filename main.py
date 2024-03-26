from fastapi import FastAPI, File, Form, UploadFile
import librosa
import asyncio
import os
from services.aubio import extract_musical_notes_aubio

from services.librosa import analyze_audio_librosa
from services.testfile import extract_musical_notes01

app = FastAPI()

@app.post("/process-audio/")
async def process_audio(file: UploadFile = File(...), description: str = Form(...)):
    # Save temporary audio file
    temp_file = f"temp_{file.filename}"
    with open(temp_file, 'wb+') as f:
        f.write(file.file.read())
    
    # Process audio to get duration
    duration = await get_audio_duration(temp_file)
    if (description == 'librosa'):
        #notes=extract_musical_notes(temp_file)
        notes = analyze_audio_librosa(temp_file)
    if(description == 'aubio'):
        notes=    extract_musical_notes_aubio(temp_file)
    # Remove temporary file
    os.remove(temp_file)
    return {"filename": file.filename, "duration": duration, "lib":description, "notes":notes}

async def get_audio_duration(file_path: str) -> float:
    # Running librosa in a threadpool to prevent blocking
    loop = asyncio.get_event_loop()
    audio_signal, sample_rate = await loop.run_in_executor(None, librosa.load, file_path)
    duration = librosa.get_duration(y=audio_signal, sr=sample_rate)
    return duration
