import json

import scenemanager

JSON_PATH: str = "levels.json"

class SaveManager:
    def __init__(self):
        self.__mJSONData = self.__load_json_data()

    def last_save(self): return self.__mJSONData["LastSave"]

    def scenes_data(self):
        data: list = {}

        for i in self.__mJSONData:
            if "Level" not in i:
                continue

            data[i] = self.__mJSONData[i]

        return data

    def save(self):
        latest_game_scene: str = scenemanager.SCENE_MANAGER.latest_game_scene()

        print(latest_game_scene)

        if latest_game_scene == "":
            return

        self.__mJSONData["LastSave"]["level"] = latest_game_scene
        self.__write_json_data()

    def __write_json_data(self):
        with open(JSON_PATH, "w+") as file:
            file.write(json.dumps(self.__mJSONData, indent=4))
            file.close()

    def __load_json_data(self):
        file = open(JSON_PATH)
        data = json.load(file)
        file.close()

        return data

SAVE_MANAGER: SaveManager = SaveManager()