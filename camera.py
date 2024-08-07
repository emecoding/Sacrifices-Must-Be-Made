import pygame

import window

class Camera:
    def __init__(self):
        self.__mOffset: list = [0, 0]

        self.__mLastPosition: list = [0, 0]

        self.__mRect: pygame.Rect = None

    def initialize(self):
        self.__mRect = pygame.Rect(0, 0, window.WINDOW.width(), window.WINDOW.height())

    def offset(self): return self.__mOffset

    def follow_player(self, player_pos: list):
        self.__mRect.centerx = player_pos[0]
        self.__mRect.centery = player_pos[1]

    def update(self):
        self.__mOffset[0] -= self.__mRect.x - self.__mLastPosition[0]
        self.__mOffset[1] -= self.__mRect.y - self.__mLastPosition[1]

        self.__mLastPosition[0] = self.__mRect.x
        self.__mLastPosition[1] = self.__mRect.y



CAMERA = Camera()