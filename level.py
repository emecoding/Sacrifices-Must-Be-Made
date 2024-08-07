import json

from gamemap import GameMap
from maploader import load_map
from enemy import Enemy, random_enemy_type

# Enemy spawn rate = how fast enemies spawn

class Level:
    def __init__(self, json_data, parent_scene):
        self.__mJSONData = json_data
        self.__mGameMap: GameMap = load_map(self.__mJSONData['map_file'])

        self.__mEnemiesSpawned: int = 0
        self.__mEnemySpawnTime: float = 0
        self.__mEnemiesKilled: int = 0

        self.__mParentScene = parent_scene

        self.__mLevelFinished: bool = False

    def game_map(self) -> GameMap: return self.__mGameMap

    def hearts_required_to_pass(self) -> int: return self.__mJSONData["hearts_required_to_pass"]

    def enemies_to_spawn(self) -> int: return self.__mJSONData["enemies_to_spawn"]

    def enemies_killed(self) -> int: return self.__mEnemiesKilled

    def level_finished(self) -> bool: return self.__mLevelFinished

    def update(self):
        self.__handle_enemy_spawning()
        self.check_for_level_finished()

    def reset(self):
        self.__mEnemiesKilled = 0
        self.__mEnemiesSpawned = 0
        self.__mLevelFinished = False

    def increment_enemies_killed(self): self.__mEnemiesKilled += 1

    def check_for_level_finished(self):
        if self.enemies_killed() == self.__mJSONData["enemies_to_spawn"]:
            self.__mParentScene.level_finished()
            self.__mLevelFinished = True

    def __handle_enemy_spawning(self):
        if self.__mEnemiesSpawned >= self.__mJSONData["enemies_to_spawn"]:
            return

        self.__mEnemySpawnTime += 1
        if self.__mEnemySpawnTime >= self.__mJSONData["enemy_spawn_rate"]:
            self.__mEnemySpawnTime = 0
            self.__spawn_enemy()

    def __spawn_enemy(self):
        self.__mEnemiesSpawned += 1

        enemy: Enemy = Enemy(self.__mGameMap.random_enemy_spawn_position(), random_enemy_type())
        self.__mParentScene.add_entity(enemy, True)



def load_level(level_name: str, parent_scene) -> Level:
    file = open("levels.json")
    data = json.load(file)
    file.close()

    level: Level = Level(data[level_name], parent_scene)
    return level
