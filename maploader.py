import pytmx

from gamemap import GameMap

MAP_PATH = "resources/maps/"

def load_map(path: str) -> GameMap:
    gameMap = GameMap(pytmx.util_pygame.load_pygame(MAP_PATH + path))
    return gameMap