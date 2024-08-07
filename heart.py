import pygame

from spritesheetloader import load_image
import renderer

class Heart:
    def __init__(self):
        self.__mSize: tuple = (17, 17)

        self.__mBackgroundImage: pygame.Surface = load_image("resources/sprites/player/heart/background.png", self.__mSize)
        self.__mBorderImage: pygame.Surface = load_image("resources/sprites/player/heart/border.png", self.__mSize)
        self.__mHeartImage: pygame.Surface = load_image("resources/sprites/player/heart/heart.png", self.__mSize)

    def render(self, filling: bool, position: tuple):
        renderer.RENDERER.draw_sprite(self.__mBackgroundImage, position, self.__mSize, use_camera=False)
        renderer.RENDERER.draw_sprite(self.__mBorderImage, position, self.__mSize, use_camera=False)
        if filling:
            renderer.RENDERER.draw_sprite(self.__mHeartImage, position, self.__mSize, use_camera=False)
