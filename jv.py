import pygame

pygame.mixer.init()

def play_sound(path: str):
    pygame.mixer.music.load(path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pass

# Главный цикл
print("Голосовой помощник запущен. Говорите!")