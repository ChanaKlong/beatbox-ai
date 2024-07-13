from utils import load_audio
import torch

model, utils = torch.hub.load(repo_or_dir='snakers4/silero-vad',
                            model='silero_vad',
                            force_reload=True)

(get_speech_timestamps, _, _, *_) = utils

def get_timstamps(path):
    y, sr = load_audio(path)
    timestamps = get_speech_timestamps(y, model, sampling_rate=sr)
    return y, sr, timestamps

