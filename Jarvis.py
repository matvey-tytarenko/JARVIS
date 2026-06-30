import random
import pyautogui as pg
import config
import pyttsx3
from datetime import datetime
import speech_recognition as sr
from groq import Groq

import jv
from voice import speak
import yaml
import webbrowser
import subprocess
import os
from jv import play_sound
import time

# Jarvis Start
play_sound(r"voices\Джарвис - приветствие.wav")

wake_words = ('джарвис', 'джар', 'джа')

# Commands load
with open("commands.yaml", 'r', encoding='utf-8') as f:
    data = yaml.safe_load(f)
COMMANDS = data["commands"]

# Random voices
sounds = [r"voices\Да сэр.wav",
          r"voices\Всегда к вашим услугам сэр.wav",
          r"voices\Есть.wav",
          r"voices\Загружаю сэр.wav",
          r"voices\Запрос выполнен сэр.wav"]

# Распознавание речи
rec = sr.Recognizer()

def listen(timeout=10, limit=10) -> str:
    with sr.Microphone() as source:
        rec.adjust_for_ambient_noise(source, duration=0.3)
        audio = rec.listen(source, timeout=timeout, phrase_time_limit=limit)
    return rec.recognize_google(audio, language='ru-RU')

# Do Commands
def run_action(action: str) -> bool:
    random_sound = random.choice(sounds)
    youtube_path = r'"C:\Program Files (x86)\Microsoft\Edge\Application\msedge_proxy.exe" --profile-directory=Default --app-id=agimnkijcaahngcdmfeangaknmldooml --app-url=https://www.youtube.com/?feature=ytca --app-launch-source=4'
    music_path = r'"C:\Program Files (x86)\Microsoft\Edge\Application\msedge_proxy.exe" --profile-directory=Default --app-id=cinhimbnkkaeohfgghhklpknlkffjgod --app-url=https://music.youtube.com/?source=pwa --app-launch-source=4'

    if action == "open_browser":
        play_sound(random_sound)
        webbrowser.open("https://www.google.com")
        return True

    elif action == "close_browser":
        play_sound(random_sound)
        os.system("taskkill /f /im firefox.exe")
        os.system("taskkill /f /im msedge.exe")
        return True

    elif action == "open_youtube":
        play_sound(random_sound)
        os.system(youtube_path)
        return True

    elif action == "open_vscode":
        play_sound(r"voices\Мы работаем над проектом сэр 2.wav")
        os.system("code")
        return True

    elif action == "open_explorer":
        play_sound(random_sound)
        os.system("explorer")
        return True

    elif action == "time":
        now = datetime.now()
        speak(f"Cейчас {now.hour} часов {now.minute} минут")
        return True

    elif action == "music":
        play_sound(random_sound)
        os.system(music_path)
        time.sleep(6)
        pg.press("space")
        return True

    elif action == "pause":
        play_sound(random_sound)
        pg.press("space")
        return True
    elif action == "restart":
        play_sound(r"voices\Отключаю питание, начинаю диагностику системы.wav")
        os.system("shutdown /r /t 0")
        return True
    elif action == "shutdown":
        play_sound(r"voices\Отключаю питание, начинаю диагностику системы.wav")
        os.system("shutdown /s /t 0")
        return True

    return False

def handle_command(text: str):
    text = text.lower()
    for keyword, value in COMMANDS.items():
        if keyword in text:
            return run_action(value['action'])
    return None

# Groq
client = Groq(api_key=config.GROQ_API)
history = []

def ask_ai(text: str) -> str:
    history.append({"role": "user", "content": text})
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=1024,
        messages=[
            {"role": "system", "content": "Ты голосовой помощник. Отвечай коротко и чётко, без markdown."},
            *history
        ]
    )
    answer = response.choices[0].message.content
    history.append({"role": "assistant", "content": answer})
    return answer

# Главный цикл
print(f"Голосовой помощник запущен. Скажите 'Джарвис' для активации.")

while True:
    try:
        # Ждём wake word
        print("Жду wake word...")
        wake_text = listen(timeout=10, limit=4).lower()
        print(f"Услышал: {wake_text}")

        if not any(w in wake_text for w in wake_words):
            continue

        # Wake word услышан
        print("Активирован! Слушаю команду...")
        play_sound(random.choice(sounds))

        # Слушаем команду
        user_input = listen(timeout=7, limit=10)
        print(f"Вы: {user_input}")

        if any(w in user_input.lower() for w in ["стоп", "выход", "пока"]):
            speak("До свидания!")
            break

        result = handle_command(user_input)
        if not result:
            answer = ask_ai(user_input)
            print(f"Ассистент: {answer}")
            speak(answer)

    except sr.WaitTimeoutError:
        pass
    except sr.UnknownValueError:
        pass
    except KeyboardInterrupt:
        print("\nОстановлено")
        break