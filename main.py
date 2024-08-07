import savemanager
import window
from scenemanager import SCENE_MANAGER
from gameinput import GAME_INPUT
from scene import Scene
from player import Player
from level import *
import renderer
import pygame
import camera
import time
from enemy import *
from mainmenu import MainMenu
from winscene import WinScene
import gametime

GAME_RUNNING: bool = True
TARGET_FPS: int = 60

def save_and_exit():
    window.WINDOW.set_background_color((127.5, 76.5, 76.5))
    window.WINDOW.fill()

    textSize: tuple = renderer.RENDERER.big_text_size("Saving...")

    renderer.RENDERER.draw_text("Saving...", (window.WINDOW.width()/2-textSize[0]/2, window.WINDOW.height()/2-textSize[1]/2), small_font=False)
    window.WINDOW.update()
    savemanager.SAVE_MANAGER.save()

    time.sleep(1)
    window.WINDOW.destroy()

def main():
    global GAME_RUNNING

    pygame.init()

    window.WINDOW = window.Window(1280, 720, "Sacrifices must be made")

    window.WINDOW.initialize()

    renderer.RENDERER = renderer.Renderer(window.WINDOW.surface())

    camera.CAMERA.initialize()

    main_menu: MainMenu = MainMenu()
    SCENE_MANAGER.add_scene(main_menu)
    SCENE_MANAGER.add_scene(WinScene())

    SCENE_MANAGER.create_scenes_from_json_file()

    #SCENE_MANAGER.set_current_scene_with_name("Win Scene")

    '''sandbox_scene: Scene = Scene("Level 0")
    sandbox_scene.set_level(load_level("Level 0"))
    SCENE_MANAGER.add_scene(sandbox_scene)

    player: Player = Player(sandbox_scene.game_map().random_spawn_point())
    sandbox_scene.add_entity(player, True)

    for i in range(0, 6):
        enemy:Enemy = Enemy([100+i*50, 500], i)
        sandbox_scene.add_entity(enemy, True)'''



    clock = pygame.time.Clock()


    while GAME_RUNNING:
        gametime.DELTA_TIME = clock.tick(TARGET_FPS)/1000


        GAME_INPUT.update_game_input()

        window.WINDOW.fill()
        SCENE_MANAGER.render_scene()
        SCENE_MANAGER.update()
        window.WINDOW.update()



        camera.CAMERA.update()

        window.WINDOW.window_input()

        GAME_RUNNING = not window.WINDOW.should_close()



    save_and_exit()

if __name__ == "__main__":
    main()