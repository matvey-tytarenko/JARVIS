import torch
import sounddevice as sd
import time

model = torch.package.PackageImporter('v4_ru.pt').load_pickle('tts_models', 'model')
model.to(torch.device('cpu'))

SPEAKER = 'aidar'
SAMPLE_RATE = 48000

def speak(text: str):
    audio = model.apply_tts(
        text=text,
        speaker=SPEAKER,
        sample_rate=SAMPLE_RATE
    )
    audio_np = audio.numpy()
    sd.play(audio_np, samplerate=SAMPLE_RATE)
    duration = len(audio_np) / SAMPLE_RATE + 1
    time.sleep(duration)