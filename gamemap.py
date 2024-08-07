import pygame
from pytmx import TiledMap
import renderer
import camera
import random
from entity import Entity

NO_COLLISIONS_LAYER: str = "NoCollisions"
COLLISIONS_LAYER: str = "Collisions"
SPAWN_POINTS_LAYER: str = "SpawnPointsLayer"
DECORATIVE_LAYER: str = "Decorative"

TILE_WIDTH = 32
TILE_HEIGHT = 32

class GameMap:
    def __init__(self, data: TiledMap):
        self.__mTiledMap: TiledMap = data

        self.__mNoCollisionsTiles: list = []
        self.__mCollisionsTiles: list = []
        self.__mDecorativeTiles: list = []
        self.__mSpawnPoints: list = []

        self.__mEntitiesToCheckCollisions: list = []

        self.__load()

    def __load(self):
        for layer in self.__mTiledMap.layers:
            if layer.name == SPAWN_POINTS_LAYER:
                for spawn_point in layer:
                    self.__mSpawnPoints.append([spawn_point.x, spawn_point.y])

                continue

            for x, y, sprite in layer.tiles():
                tile = [x, y, sprite]
                if layer.name == NO_COLLISIONS_LAYER:
                    self.__mNoCollisionsTiles.append(tile)
                elif layer.name == COLLISIONS_LAYER:
                    self.__mCollisionsTiles.append(tile)
                elif layer.name == DECORATIVE_LAYER:
                    self.__mDecorativeTiles.append(tile)
                else:
                    print(f"Layer name '{layer.name}' is not valid!")

    def __render_tile(self, tile: list):
        renderer.RENDERER.draw_sprite(tile[2], (tile[0]*TILE_WIDTH, tile[1]*TILE_HEIGHT), (TILE_WIDTH, TILE_HEIGHT))

    def __render_layer(self, layer: list):
        for tile in layer:
            self.__render_tile(tile)

    def remove_entity_from_collisions(self, entity: Entity):
        if entity in self.__mEntitiesToCheckCollisions:
            self.__mEntitiesToCheckCollisions.remove(entity)

    def clear_collisions(self):
        self.__mEntitiesToCheckCollisions.clear()

    def check_for_collisions(self):
        camera_offset = camera.CAMERA.offset()
        for entity in self.__mEntitiesToCheckCollisions:
            for tile_x, tile_y, tile_sprite in self.__mCollisionsTiles:
                final_tile_x = tile_x*TILE_WIDTH
                final_tile_y = tile_y*TILE_HEIGHT
                tile_rect = (final_tile_x, final_tile_y, TILE_WIDTH, TILE_HEIGHT)

                rect: pygame.Rect = entity.get_rect()
                x_rect: pygame.Rect = pygame.Rect(rect.x + entity.mAcceleration.x * entity.mSpeed, rect.y, rect.w, rect.h)
                y_rect: pygame.Rect = pygame.Rect(rect.x, rect.y + entity.mAcceleration.y * entity.mSpeed, rect.w, rect.h)

                has_had_collision_with_tile: bool = False

                if x_rect.colliderect(tile_rect):
                    has_had_collision_with_tile = True

                    if entity.mRect.x < final_tile_x and entity.mAcceleration.x > 0: #Is on left side and is moving right
                        entity.mAcceleration.x = 0
                    if entity.mRect.x > final_tile_x and entity.mAcceleration.x < 0: # Is on right side and is moving left
                        entity.mAcceleration.x = 0

                if y_rect.colliderect(tile_rect):
                    has_had_collision_with_tile = True

                    if entity.mRect.y < final_tile_y and entity.mAcceleration.y > 0: # Is on top and is moving down
                        entity.mAcceleration.y = 0
                    if entity.mRect.y > final_tile_y and entity.mAcceleration.y < 0: #Is below and is moving up
                        entity.mAcceleration.y = 0

                if has_had_collision_with_tile: entity.on_collision_with_tile()

            entity.apply_acceleration()

    def render(self):
        self.__render_layer(self.__mNoCollisionsTiles)
        self.__render_layer(self.__mCollisionsTiles)
        self.__render_layer(self.__mDecorativeTiles)

    def random_spawn_point(self):
        if len(self.__mSpawnPoints) == 0:
            print("No spawn points found...")
            return [0, 0]
        return random.choice(self.__mSpawnPoints)

    def random_enemy_spawn_position(self):
        tile: list = random.choice(self.__mNoCollisionsTiles)
        return [tile[0]*TILE_WIDTH, tile[1]*TILE_HEIGHT]
        #return [random.randint(TILE_WIDTH, (self.__mTiledMap.width-1)*TILE_WIDTH), random.randint(TILE_HEIGHT, (self.__mTiledMap.height-1)*TILE_HEIGHT)]

    def add_entity_to_check_collisions_for(self, entity: Entity):
        self.__mEntitiesToCheckCollisions.append(entity)

    def width(self) -> int: return self.__mTiledMap.width * TILE_WIDTH
    def height(self) -> int: return self.__mTiledMap.height * TILE_HEIGHT
