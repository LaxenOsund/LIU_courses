import pygame
import os

pygame.mixer.init()

main_dir = os.path.split(os.path.abspath(__file__))[0]

def load_music(file):
    """ Loads background musik from the data directory. """
    file = os.path.join(main_dir, 'data', file)
    pygame.mixer.music.load(file)
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1)
    


def load_sound(file):
    """ Loads a sound effect from the data directory. """
    file = os.path.join(main_dir, 'data', file)
    return pygame.mixer.Sound(file)


shoot_sound = load_sound("saul.wav")

hit_tank_sound = load_sound("bonk.wav")

kill_tank_sound = load_sound("death.wav")

hit_box_sound = load_sound("bloon.wav")

