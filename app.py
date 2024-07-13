from utils import load_audio, save_audio, split_from_mask
from vad import get_timstamps
import gradio as gr
import numpy as np


def perform_voice_enhacement(path):
    y, sr, timestamps = get_timstamps(path)

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

    return (sr, y)


demo = gr.Interface(
    fn=perform_voice_enhacement,
    inputs=gr.Audio(type="filepath", label="Upload audio file"),
    outputs="audio",
)

demo.launch()
