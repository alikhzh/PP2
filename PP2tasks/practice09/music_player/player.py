import pygame
import os

class Player:
    def __init__(self):
        self.tracks = []
        self.cur = 0
        self.playing = False
        
    def load(self, folder):
        self.tracks = []
        files = os.listdir(folder)
        for file in files:
            if file.endswith('.mp3'):
                self.tracks.append(os.path.join(folder, file))
        
        if self.tracks:
            pygame.mixer.music.load(self.tracks[0])

    def play(self):
        if self.tracks:
            pygame.mixer.music.load(self.tracks[self.cur])
            pygame.mixer.music.play()
            self.playing = True

    def stop(self):
        pygame.mixer.music.stop()
        self.playing = False

    def next(self):
        if self.tracks:
            self.cur = (self.cur + 1) % len(self.tracks)
            self.play()

    def pre(self):
        if self.tracks:
            self.cur = (self.cur - 1) % len(self.tracks)
            self.play()