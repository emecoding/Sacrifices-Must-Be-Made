from scene import Scene
import window
import savemanager
from level import load_level

class SceneManager:
    def __init__(self):
        self.__mScenes: list = []

        self.__mCurrentSceneIndex: int = 0
        self.__mLatestGameScene: str = ""

    def add_scene(self, scene: Scene):
        self.__mScenes.append(scene)

        if len(self.__mScenes) == 1:
            self.set_current_scene(0)

    def set_current_scene(self, index: int):
        self.__mCurrentSceneIndex = index

        name = self.__mScenes[self.__mCurrentSceneIndex].name()
        if "Level" in name:
            self.__mLatestGameScene = name

        window.WINDOW.update_caption(self.__mScenes[self.__mCurrentSceneIndex].name())

    def set_current_scene_with_name(self, name: str):
        for i in range(0, len(self.__mScenes)):
            if self.__mScenes[i].name() == name:
                self.set_current_scene(i)
                return

    def set_current_scene_to_first_game_level(self):
        self.set_current_scene_with_name("Level 0")

    def get_current_scene(self):
        return self.__mScenes[self.__mCurrentSceneIndex]

    def latest_game_scene(self) -> str: return self.__mLatestGameScene

    def create_scenes_from_json_file(self):
        scenes_data = savemanager.SAVE_MANAGER.scenes_data()

        for scene_name in scenes_data:
            scene: Scene = Scene(scene_name)
            scene.set_level(load_level(scene_name, scene))
            scene.create_needed_entities()

            self.add_scene(scene)

    def load_next_game_scene(self):
        if self.__mCurrentSceneIndex >= len(self.__mScenes)-1:
            self.set_current_scene_with_name("Win Scene")
        else:
            self.set_current_scene(self.__mCurrentSceneIndex+1)

    def load_current_scene_again(self):
        self.__mScenes[self.__mCurrentSceneIndex].destroy_entities()
        self.__mScenes[self.__mCurrentSceneIndex].create_needed_entities()
        self.__mScenes[self.__mCurrentSceneIndex].level().reset()
        self.__mScenes[self.__mCurrentSceneIndex].play()

    def load_scene_from_save(self, save):
        self.set_current_scene_with_name(save["level"])

    def update(self):
        self.__mScenes[self.__mCurrentSceneIndex].update()

    def render_scene(self):
        self.__mScenes[self.__mCurrentSceneIndex].render()

SCENE_MANAGER = SceneManager()