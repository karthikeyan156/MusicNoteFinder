from fastapi import FastAPI, File, UploadFile
import librosa
import asyncio
import os

app = FastAPI()

@app.post("/process-audio/")
async def process_audio(file: UploadFile = File(...)):
    # Save temporary audio file
    temp_file = f"temp_{file.filename}"
    with open(temp_file, 'wb+') as f:
        f.write(file.file.read())
    
    # Process audio to get duration
    duration = await get_audio_duration(temp_file)
    
    # Remove temporary file
    os.remove(temp_file)
    
    return {"filename": file.filename, "duration": duration}

async def get_audio_duration(file_path: str) -> float:
    # Running librosa in a threadpool to prevent blocking
    loop = asyncio.get_event_loop()
    audio_signal, sample_rate = await loop.run_in_executor(None, librosa.load, file_path)
    duration = librosa.get_duration(y=audio_signal, sr=sample_rate)
    print(duration)
    return duration
