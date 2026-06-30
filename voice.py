import torch
import sounddevice as sd
import time
import re
from num2words import num2words

model = torch.package.PackageImporter('v4_ru.pt').load_pickle('tts_models', 'model')
model.to(torch.device('cpu'))

SPEAKER = 'aidar'
SAMPLE_RATE = 48000

def numbers_to_words(text: str) -> str:
    def replace(match):
        num = match.group()
        try:
            return num2words(int(num), lang='ru')
        except ValueError:
            return num
    return re.sub(r'\d+', replace, text)

def clean_text(text: str) -> str:
    text = re.sub(r'[*_#`~\[\]]', '', text)
    text = numbers_to_words(text)
    text = re.sub(r'[^\w\sа-яА-ЯёЁ.,!?:;\-]', '', text)
    return text.strip()

def speak(text: str):
    text = clean_text(text)
    if not text:
        return

    try:
        audio = model.apply_tts(
            text=text,
            speaker=SPEAKER,
            sample_rate=SAMPLE_RATE
        )
        audio_np = audio.numpy()
        sd.play(audio_np, samplerate=SAMPLE_RATE)
        duration = len(audio_np) / SAMPLE_RATE + 1
        time.sleep(duration)
    except ValueError:
        print(f"Не удалось озвучить: {text}")