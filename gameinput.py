import pygame

UP_KEY = pygame.K_UP
DOWN_KEY = pygame.K_DOWN
LEFT_KEY = pygame.K_LEFT
RIGHT_KEY = pygame.K_RIGHT
ATTACK_KEY = pygame.K_z
PICK_UP_KEY = pygame.K_x
GIVE_UP_KEY = pygame.K_r

class GameInput:
    def __init__(self):
        self.__mKeyboardKeys: dict = None

    def update_game_input(self):
        self.__mKeyboardKeys = pygame.key.get_pressed()

    def keyboard_key_pressed(self, key: int): return self.__mKeyboardKeys[key]

GAME_INPUT = GameInput()