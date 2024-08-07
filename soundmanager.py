import os
import random

import pygame

pygame.mixer.init()

SOUNDS_PATH: str = "resources/sounds/"

#, miss

#https://pixabay.com/sound-effects/search/game/

class SoundManager:
    def __init__(self):
        self.__mSounds: dict = self.__read_sound_files()

        self.__mSoundEffectVolume: float = 1.0
        self.__mBackgroundMusicVolume: float = 1.0
        self.set_sound_effect_volume(0.1) #0.1
        self.set_background_music_volume(0.05) #0.1

    def __read_sound_files(self) -> dict:
        final_data: dict = {}
        folders: list = os.listdir(SOUNDS_PATH)

        pygame.mixer.set_num_channels(len(folders))

        channel: int = 0

        for folder in folders:
            sounds: list = [channel] #Channel, sound files
            files: list = os.listdir(SOUNDS_PATH + folder)

            for file in files:
                sound_file: pygame.mixer.Sound = pygame.mixer.Sound(f"{SOUNDS_PATH}{folder}/{file}")
                sounds.append(sound_file)

            channel += 1
            final_data[folder] = sounds

        return final_data

    def play_random_sound(self, sound_name: str, volume: float, loop:int=0):
        sound: pygame.mixer.Sound = self.__mSounds[sound_name][random.randint(1, len(self.__mSounds[sound_name])-1)]
        channel_num: int = self.__mSounds[sound_name][0]
        channel: pygame.mixer.Channel = pygame.mixer.Channel(channel_num)

        channel.set_volume(volume)
        channel.play(sound, loops=loop)

    def set_sound_effect_volume(self, volume: float):
        self.__mSoundEffectVolume = volume

    def set_background_music_volume(self, volume: float):
        self.__mBackgroundMusicVolume = volume

    def sound_effect_volume(self) -> float: return self.__mSoundEffectVolume
    def background_music_volume(self) -> float: return self.__mBackgroundMusicVolume


SOUND_MANAGER: SoundManager = SoundManager()
