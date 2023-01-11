import pygame

class Sound():
    def __init__(self,id_channel,sounds):
        pygame.init()
        self.channel = pygame.mixer.Channel(id_channel)
        self.get_sounds(sounds)


    def get_sounds(self,sounds):
        self.sounds = {}
        for key in sounds:
           self.sounds[key] = pygame.mixer.Sound(sounds[key])

    
    def play(self, sound):
        self.channel.play(sound)


