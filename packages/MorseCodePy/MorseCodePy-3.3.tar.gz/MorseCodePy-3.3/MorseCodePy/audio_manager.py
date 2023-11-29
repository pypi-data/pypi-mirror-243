# Hide the pygame support prompt
from os import environ

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

from pygame import mixer
from os import path
from time import sleep


class AudioManager:
    def __init__(self, directory: str = 'sounds', extension: str = '.wav'):
        self.__directory = directory
        self.__extension = extension.lower()

        mixer.init()  # Initialize pygame mixer

    def play_dot(self) -> None:
        dot_sound_path = path.join(path.dirname(__file__), self.__directory, f'dot{self.__extension}')

        mixer.music.load(dot_sound_path)
        mixer.music.play()
        sleep(0.09)

    def play_dash(self) -> None:
        dash_sound_path = path.join(path.dirname(__file__), self.__directory, f'dash{self.__extension}')

        mixer.music.load(dash_sound_path)
        mixer.music.play()
        sleep(0.24)
