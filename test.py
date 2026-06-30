import speech_recognition as sr

recognizer = sr.Recognizer()


def listen():
    with sr.Microphone() as source:
        print("Настройка под шум окружения...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Говорите!")

        try:
            audio = recognizer.listen(source, timeout=5)
            print("Распознаю...")
            text = recognizer.recognize_google(audio, language="ru-RU")
            print(f"Вы сказали: {text}")
            return text

        except sr.WaitTimeoutError:
            print("Тишина — ничего не услышал")
        except sr.UnknownValueError:
            print("Не удалось распознать речь")
        except sr.RequestError as e:
            print(f"Ошибка сервиса Google: {e}")


while True:
    listen()
    print("-" * 30)