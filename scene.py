import pygame

import renderer
import scenemanager
from entity import Entity
from level import Level
from player import Player
from spritesheetloader import load_image
from button import Button, ACTIVE_COLOR
from gameinput import GAME_INPUT, PICK_UP_KEY
import window

class Scene:
    def __init__(self, name: str):
        self.__mName: str = name

        self.__mEntities: list = []
        self.__mEnemyEntities: list = []

        self.__mButtons: list = []
        self.__mJustPressedButton: bool = False

        self.__mPlayer: Player = None

        self.__mBackgroundColor: tuple = (0, 0, 0)
        self.__mLevel: Level = None

        self.__mIsPlaying: bool = True

        self.__mMenuPanelSize: tuple = (47*2, 60*2)
        self.__mMenuPanel: pygame.Surface = load_image("resources/sprites/menu/panel.png", self.__mMenuPanelSize)

    def set_level(self, level: Level): self.__mLevel = level

    def set_background_color(self, color: tuple): self.__mBackgroundColor = color

    def pause(self): self.__mIsPlaying = False

    def play(self): self.__mIsPlaying = True

    def level_finished(self):
        self.pause()

    def name(self): return self.__mName

    def level(self) -> Level: return self.__mLevel

    def add_entity(self, entity: Entity, collisions: bool):
        self.__mEntities.append(entity)
        if entity.mTag == "ENEMY":
            self.__mEnemyEntities.append(entity)

        if collisions and self.__mLevel != None:
            self.__mLevel.game_map().add_entity_to_check_collisions_for(entity)

    def update(self):
        if self.__mIsPlaying:
            for entity in self.__mEntities:
                entity.update()

            if self.__mLevel is not None:
                self.__mLevel.update()
                self.__mLevel.game_map().check_for_collisions()

        if self.__mPlayer != None:
            if self.__mPlayer.is_dead() or self.__mPlayer.given_up():
                self.pause()



    def enemy_entities(self):
        return self.__mEnemyEntities

    def get_entity_with_tag(self, tag: str) -> Entity:
        for entity in self.__mEntities:
            if entity.mTag == tag: return entity

        return None

    def destroy_entities(self):
        self.__mPlayer = None

        self.__mEntities.clear()
        self.__mEnemyEntities.clear()
        self.__mLevel.game_map().clear_collisions()

    def remove_entity(self, entity: Entity):
        self.__mEntities.remove(entity)
        if entity.mTag == "ENEMY":
            self.__mEnemyEntities.remove(entity)

    def create_needed_entities(self):
        if self.__mLevel is None:
            print(f"Failed to create needed entities for {self.__mName}. No level set.")
            return

        self.__mPlayer = Player(self.__mLevel.game_map().random_spawn_point())
        self.add_entity(self.__mPlayer, True)

    def render(self):
        window.WINDOW.set_background_color(self.__mBackgroundColor)
        if self.__mLevel is not None:
            self.__mLevel.game_map().render()
            renderer.RENDERER.draw_text(f"Hearts Required: {self.__mLevel.hearts_required_to_pass()}", (10, 30))
            renderer.RENDERER.draw_text(f"Enemies Killed: {self.__mLevel.enemies_killed()}", (10, 50))
            renderer.RENDERER.draw_text(f"Enemies Left: {self.__mLevel.enemies_to_spawn()-self.__mLevel.enemies_killed()}", (10, 70))

        for entity in self.__mEntities:
            entity.render()

        if self.__mLevel != None and self.__mPlayer != None:
            if self.__mLevel.level_finished() or self.__mPlayer.is_dead() or self.__mPlayer.given_up():
                window_width = window.WINDOW.width()
                window_height = window.WINDOW.height()
                text0Size: tuple = renderer.RENDERER.big_text_size("Level Finished")
                text1Size: tuple = renderer.RENDERER.big_text_size("Next Level Accomplished")
                text2Size: tuple = renderer.RENDERER.big_text_size("Not Enough Hearts Left")
                text3Size: tuple = renderer.RENDERER.big_text_size("Try Again")
                text4Size: tuple = renderer.RENDERER.big_text_size("Continue")
                text5Size: tuple = renderer.RENDERER.big_text_size("You Died!")
                text6Size: tuple = renderer.RENDERER.big_text_size("You Gave Up!")

                renderer.RENDERER.draw_text("Level Finished", (window_width/2-text0Size[0]/2, window_height/2-text0Size[1]/2 - 200), small_font=False)

                if not self.__mPlayer.is_dead():
                    if self.__mPlayer.given_up():
                        renderer.RENDERER.draw_text("You Gave Up!", (window_width/2-text6Size[0]/2, window_height/2-text6Size[1]/2 - 150), small_font=False)
                        self.__mButtons.insert(0, Button("Try Again", lambda: scenemanager.SCENE_MANAGER.load_current_scene_again(), (window_width/2-text3Size[0]/2, window_height/2-text3Size[1]/2 - 70)))
                    else:
                        if self.__mPlayer.current_hearts() >= self.__mLevel.hearts_required_to_pass():
                            renderer.RENDERER.draw_text("Next Level Accomplished", (window_width/2-text1Size[0]/2, window_height/2-text1Size[1]/2 - 150), small_font=False)
                            self.__mButtons.insert(0, Button("Continue", lambda: scenemanager.SCENE_MANAGER.load_next_game_scene(), (window_width/2-text4Size[0]/2, window_height/2-text4Size[1]/2 - 70)))
                        else:
                            renderer.RENDERER.draw_text("Not Enough Hearts Left", (window_width/2-text2Size[0]/2, window_height/2-text2Size[1]/2 - 120), small_font=False)
                            self.__mButtons.insert(0, Button("Try Again", lambda: scenemanager.SCENE_MANAGER.load_current_scene_again(), (window_width/2-text3Size[0]/2, window_height/2-text3Size[1]/2 - 70)))
                else:
                    renderer.RENDERER.draw_text("You Died!", (window_width/2-text5Size[0]/2, window_height/2-text5Size[1]/2 - 120), small_font=False)
                    self.__mButtons.insert(0, Button("Try Again", lambda: scenemanager.SCENE_MANAGER.load_current_scene_again(), (window_width/2-text3Size[0]/2, window_height/2-text3Size[1]/2 - 70)))


                self.__mButtons[0].render(True, text4Size)

                if GAME_INPUT.keyboard_key_pressed(PICK_UP_KEY) and not self.__mJustPressedButton:
                    self.__mJustPressedButton = True
                    self.__mButtons[0].pressed()

                if not GAME_INPUT.keyboard_key_pressed(PICK_UP_KEY):
                    self.__mJustPressedButton = False


    def game_map(self): return self.__mLevel.game_map()