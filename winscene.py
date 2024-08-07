import renderer
import scenemanager
import window
from scene import Scene
from button import Button
from gameinput import *
import soundmanager

class WinScene(Scene):
    def __init__(self):
        super().__init__("Win Scene")

        self.__mStartY: int = 200
        self.__mTexts: list = []


        self.__add_text("You Won!")
        self.__add_text("Press 'ESC' To Exit")

    def __add_text(self, text: str):
        textSize: tuple = renderer.RENDERER.big_text_size(text)
        window_width: int = window.WINDOW.width()

        self.__mTexts.append([text, window_width/2-textSize[0]/2, self.__mStartY + 80*len(self.__mTexts)])

    def render(self):
        window.WINDOW.set_background_color((127.5, 76.5, 76.5))
        for text in self.__mTexts:
            renderer.RENDERER.draw_text(text[0], (text[1], text[2]), small_font=False)



