import pygame
import camera

from window import WINDOW

class Renderer:
    def __init__(self, window: pygame.Surface):
        self.__mSurface: pygame.Surface = window

        self.__mSmallFontSize: int = 32
        self.__mSmallFont: pygame.font.Font = pygame.font.Font("resources/fonts/Silver.ttf", self.__mSmallFontSize)

        self.__mBigFontSize: int = 64
        self.__mBigFont: pygame.font.Font = pygame.font.Font("resources/fonts/Silver.ttf", self.__mBigFontSize)
    def draw_rect(self, rect: pygame.Rect, color: tuple, size:int = 1, use_camera:bool = True):
        x = rect.x
        y = rect.y
        if use_camera:
            camera_offset = camera.CAMERA.offset()
            x += camera_offset[0]
            y += camera_offset[1]

        pygame.draw.rect(self.__mSurface, color, (x, y, rect.w, rect.h), size)

    def draw_sprite(self, sprite: pygame.Surface, pos: list, size: tuple, scale: float = 1, use_camera: bool = True):
        sprite = pygame.transform.scale_by(sprite, scale)
        final_sprite = sprite
        if size[0] > 0 and size[1] > 0:
            final_sprite: pygame.Surface = pygame.transform.scale(sprite, size)
        final_position = [pos[0], pos[1]]
        if use_camera:
            camera_offset = camera.CAMERA.offset()
            final_position[0] += camera_offset[0]
            final_position[1] += camera_offset[1]
        self.__mSurface.blit(final_sprite, final_position)

    def draw_text(self, data: str, position: tuple, anti_alias: bool=True, color: tuple = (255, 255, 255), size: tuple = None, small_font: bool = True):
        text = None
        if small_font:
            text = self.__mSmallFont.render(data, anti_alias, color)
        else:
            text = self.__mBigFont.render(data, anti_alias, color)

        if size is not None:
            text = pygame.transform.scale(text, size)
        self.__mSurface.blit(text, position)

    def small_font_size(self) -> int: return self.__mSmallFontSize

    def small_text_size(self, text: str) -> tuple: return self.__mSmallFont.size(text)

    def big_font_size(self) -> int: return self.__mBigFontSize

    def big_text_size(self, text: str) -> tuple: return self.__mBigFont.size(text)


RENDERER: Renderer = None