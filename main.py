from fastapi import FastAPI, File, UploadFile
import librosa
import asyncio

app = FastAPI()

@app.post("/process-audio/")
async def process_audio(file: UploadFile = File(...)):
    # Save temporary audio file
    temp_file = f"temp_{file.filename}"
    with open(temp_file, 'wb+') as f:
        f.write(file.file.read())
    
    # Process audio to get duration
    duration = await get_audio_duration(temp_file)
    
    # Remove temporary file if needed
    # os.remove(temp_file)
    
    return {"filename": file.filename, "duration": duration}

async def get_audio_duration(file_path: str) -> float:
    # Running librosa in a threadpool to prevent blocking
    loop = asyncio.get_event_loop()
    duration = await loop.run_in_executor(None, librosa.get_duration(filename=file_path), file_path)
    print(duration)
    return duration
