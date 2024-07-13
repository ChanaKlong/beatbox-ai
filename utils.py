import librosa
import soundfile as sf
import numpy as np
import random


def load_audio(path):
    y, sr = librosa.load(path, sr=16000)
    return y, sr


def save_audio(path, y, sr):
    sf.write(path, y, sr)


def split_from_mask(y, mask, sr):
    chunks = []

    start = 0
    end = 0
    for i in range(len(mask)):
        if mask[i] == 1:
            if start == 0:
                start = i
            end = i
        else:
            if start != 0 and (end - start) / sr > 0.075:
                chunks.append((start, end))
                start = 0
                end = 0

    chunks = reversed(chunks)

    for start, end in chunks:
        beatbox = find_beatbox_sound(y[start:end], sr)
        y = np.concatenate((y[:start], beatbox, y[end:]))

    return y


def vectorize(y, sr=16000):
    y = librosa.feature.chroma_stft(y=y, sr=sr)
    y = np.mean(y, axis=1)
    return y


beatbox_sounds = [load_audio(f"./beatbox_sounds/{i:02d}.wav")[0] for i in range(1, 24)]


def consine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def find_beatbox_sound(y, sr):
    y = vectorize(y, sr)

    similarities = [
        consine_similarity(y, vectorize(beatbox)) for beatbox in beatbox_sounds
    ]

    most_similar = np.argmax(similarities)

    return beatbox_sounds[most_similar]
