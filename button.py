import renderer
import soundmanager

ACTIVE_COLOR: tuple = (110, 105, 103)
NON_ACTIVE_COLOR: tuple = (255, 255, 255)

class Button:
    def __init__(self, text: str, function, pos: list):
        self.__mText: str = text
        self.__mFunction = function
        self.__mPosition: list = pos

    def pressed(self):
        self.__mFunction()
        soundmanager.SOUND_MANAGER.play_random_sound("buttonclick", soundmanager.SOUND_MANAGER.sound_effect_volume())

    def position(self): return self.__mPosition

    def text(self) -> str: return self.__mText


    def render(self, is_active: bool, size: tuple):
        renderer.RENDERER.draw_text(self.__mText, self.__mPosition, color=(ACTIVE_COLOR if is_active else NON_ACTIVE_COLOR), size=size, small_font=False)