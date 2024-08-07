import renderer
import savemanager
from scene import Scene
from button import Button
import window
from gameinput import *
from spritesheetloader import load_sprite_sheet
import scenemanager
import soundmanager

# A picture of a map and player as the background image. Make with gimp

class MainMenu(Scene):
    def __init__(self):
        super().__init__("Main Menu")
        self.__mButtons: list = []
        self.__mActiveButton: int = 0
        self.__mButtonOffsetY: float = 50
        self.__mButtonStartY: float = 200

        self.__mJustMoved: bool = False
        self.__mJustPressed: bool = False

        self.__mKeyboardIconSize: tuple = (20, 18)
        self.__mKeyboardIconsSpriteSheet: list = load_sprite_sheet("keyboard/icons.png",125/8, 107/7, 54)

        self.__mTitlePositionY: float = 20
        self.__mTitle: str = "Sacrifices Must Be Made"
        self.__mTitleColor: tuple = (117, 12, 21)

        self.set_background_color((127.5, 76.5, 76.5))

        soundmanager.SOUND_MANAGER.play_random_sound("background", soundmanager.SOUND_MANAGER.background_music_volume(), loop=-1)

        self.__set_up_GUI()

    def __set_up_GUI(self):
        self.__mButtons.append(Button("New Game", lambda: scenemanager.SCENE_MANAGER.set_current_scene_to_first_game_level(), [self.__button_x("New Game"), self.__mButtonStartY]))
        self.__mButtons.append(Button("Continue", lambda: scenemanager.SCENE_MANAGER.load_scene_from_save(savemanager.SAVE_MANAGER.last_save()), [self.__button_x("Continue"), self.__mButtonStartY+self.__mButtonOffsetY]))
        self.__mButtons.append(Button("Settings", lambda: print("Settings"), [self.__button_x("Settings"), self.__mButtonStartY+self.__mButtonOffsetY*2]))
        self.__mButtons.append(Button("Exit", lambda: window.WINDOW.set_window_should_close(True), [self.__button_x("Exit"), self.__mButtonStartY+self.__mButtonOffsetY*3]))

    def __button_x(self, text: str):
        return window.WINDOW.width()/2 - renderer.RENDERER.big_text_size(text)[0]/2

    def __main_menu_input(self):
        if GAME_INPUT.keyboard_key_pressed(DOWN_KEY) and not self.__mJustMoved:
            self.__mJustMoved = True
            self.__mActiveButton += 1
            soundmanager.SOUND_MANAGER.play_random_sound("buttonclick", soundmanager.SOUND_MANAGER.sound_effect_volume())

        if GAME_INPUT.keyboard_key_pressed(UP_KEY) and not self.__mJustMoved:
            self.__mJustMoved = True
            self.__mActiveButton -= 1
            soundmanager.SOUND_MANAGER.play_random_sound("buttonclick", soundmanager.SOUND_MANAGER.sound_effect_volume())

        if not GAME_INPUT.keyboard_key_pressed(DOWN_KEY) and not GAME_INPUT.keyboard_key_pressed(UP_KEY):
            self.__mJustMoved = False

        if self.__mActiveButton > len(self.__mButtons) - 1:
            self.__mActiveButton = 0

        if self.__mActiveButton < 0:
            self.__mActiveButton = len(self.__mButtons) - 1

        if GAME_INPUT.keyboard_key_pressed(PICK_UP_KEY) and not self.__mJustPressed:
            self.__mButtons[self.__mActiveButton].pressed()
            self.__mJustPressed = True

        if not GAME_INPUT.keyboard_key_pressed(PICK_UP_KEY):
            self.__mJustPressed = False

    def __keyboard_icon_position(self, button: Button, icon_type: int) -> list:
        button_size: tuple = renderer.RENDERER.big_text_size(button.text())
        button_position: list = button.position()
        icon_offset_x: float = 6
        icon_offset_y: float = 10
        if icon_type == UP_KEY:
            return [button_position[0] + button_size[0] + icon_offset_x, button_position[1] + icon_offset_y]
        elif icon_type == DOWN_KEY:
            return [button_position[0] + button_size[0] + icon_offset_x, button_position[1] + self.__mKeyboardIconSize[1] + icon_offset_y]
        elif icon_type == PICK_UP_KEY:
            return [button_position[0] - self.__mKeyboardIconSize[0] - icon_offset_x, button_position[1] + self.__mKeyboardIconSize[1]/4 + icon_offset_y]
        return button_position

    def __render_main_menu(self):
        renderer.RENDERER.draw_text(self.__mTitle, (self.__button_x(self.__mTitle), self.__mTitlePositionY), small_font=False, color=self.__mTitleColor)

        for i in range(0, len(self.__mButtons)):
            is_active: bool = (i == self.__mActiveButton)
            self.__mButtons[i].render(is_active, None)
            if is_active:
                renderer.RENDERER.draw_sprite(self.__mKeyboardIconsSpriteSheet[0], self.__keyboard_icon_position(self.__mButtons[i], UP_KEY), self.__mKeyboardIconSize)
                renderer.RENDERER.draw_sprite(self.__mKeyboardIconsSpriteSheet[1], self.__keyboard_icon_position(self.__mButtons[i], DOWN_KEY), self.__mKeyboardIconSize)
                renderer.RENDERER.draw_sprite(self.__mKeyboardIconsSpriteSheet[39], self.__keyboard_icon_position(self.__mButtons[i], PICK_UP_KEY), self.__mKeyboardIconSize)



    def update(self):
        self.__main_menu_input()
        self.__render_main_menu()




