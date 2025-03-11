# Credits: Jonas
import pygame

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        pygame.mixer.set_num_channels(16)
        self.sounds = {}
        self.music_volume = 0.2
        self.sfx_volume = 0.5
    
    # SFX
    def load_sfx(self, name, path):
        self.sounds[name] = pygame.mixer.Sound(f'../sounds/sfx/{path}')
        self.sounds[name].set_volume(self.sfx_volume)
    
    def play_sfx(self, name):
        if name in self.sounds:
            self.sounds[name].play()
    
    def set_sfx_volume(self, volume):
        self.sfx_volume = volume
        for sound in self.sounds.values():
            sound.set_volume(self.sfx_volume)
    
    # Music    
    def play_music(self, path, loop=-1):
        pygame.mixer.music.load(f'../sounds/music/{path}')
        pygame.mixer.music.set_volume(self.music_volume)
        pygame.mixer.music.play(loop)
    
    def stop_music(self):
        pygame.mixer.music.stop()
    
    def set_music_volume(self, volume):
        self.music_volume = max(0, min(1, volume))
        pygame.mixer.music.set_volume(self.music_volume)
    
    def is_music_playing(self):
        return pygame.mixer.music.get_busy()
