from typing import Any
import pygame
import PySimpleGUI as sg

class Sound:
    def __init__(self, path):
        self.music = pygame.mixer_music.load(path)
        self.music_volume = pygame.mixer.music.set_volume(0.25)
        self.music_play = pygame.mixer.music.play(loops=-1)
        self.state = True
        self.state2 = 1

    def music_on_off(self):
        if not self.state:            
            self.music_volume = pygame.mixer.music.set_volume(0.25)
            self.state = True
        else:
            self.music_volume = pygame.mixer.music.set_volume(0.0)
            self.state = False

    def change_theme(self):
        if not self.state2 == 1:            
            self.music = pygame.mixer_music.load("python/music/theme1.mp3")
            self.state2 = 1
            pygame.mixer.music.play(loops=-1)
        else:
            self.music = pygame.mixer_music.load("python/music/theme2.mp3")
            self.state2 = 2
            pygame.mixer.music.play(loops=-1)

    def popup_infos(self):
        sg.popup("HOTKEYS:\nP = Pause/Play\nM = Change music\nI = Show this window (Infos)")