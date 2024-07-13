from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from utils import load_audio, save_audio, split_from_mask
from vad import get_timstamps
import numpy as np
import tempfile
import os

app = FastAPI()

@app.post("/enhance-voice/")
async def enhance_voice(sound: UploadFile = File(...)):
    # Save the uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
        temp_file.write(await sound.read())
        temp_path = temp_file.name

    y, sr, timestamps = get_timstamps(temp_path)

    timestamps = sorted(timestamps, key=lambda x: -x["start"])

    chunks = []
    for ts in timestamps:
        chunk = y[ts["start"] : ts["end"]]
        print(len(chunk) / sr)
        chunks.append(chunk)

    for chunk, ts in zip(chunks, timestamps):
        mask = chunk > 0.1
        chunk = chunk * mask
        beatbox = split_from_mask(chunk, mask, sr)
        y = np.concatenate((y[: ts["start"]], beatbox, y[ts["end"] :]))

    output_path = tempfile.mktemp(suffix=".wav")
    save_audio(output_path, y, sr)

    os.unlink(temp_path)

    return FileResponse(output_path, media_type="audio/wav", filename="enhanced_audio.wav")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)