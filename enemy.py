import random

import gametime
from entity import Entity
from animator import Animator
from spritesheetloader import load_sprite_sheet, get_sprites_from_index_A_to_index_B, load_image
import scenemanager
import camera
import soundmanager
import renderer
import pygame
from player import Player
import math
import os

# Enemy types
BLUE_BIRD_ENEMY: int = 0
WHITE_BIRD_ENEMY: int = 1
GRAY_CAT_ENEMY: int = 2
ORANGE_CAT_ENEMY: int = 3
FOX_ENEMY: int = 4
RACCOON_ENEMY: int = 5

# Enemy speeds
FAST_SPEED: float = 75
SLOW_SPEED: float = 50

# Enemy healths
LOW_HEALTH: float = 3
HIGH_HEALTH: float = 5

# Enemy knock backs
LITTLE_KNOCK_BACK: float = 3
NORMAL_KNOCK_BACK: float = LITTLE_KNOCK_BACK*2
HIGH_KNOCK_BACK: float = LITTLE_KNOCK_BACK*3

# Enemy damages
LOW_DAMAGE: int = 1
HIGH_DAMAGE: int = 2

# Blue bird fast, but low health. Normal knock back and little damage.
# White bird slow, but lots of health. Little knock back and damage.
# Gray cat fast, but low health. Little knock back, but high damage.
# Orange cat fast, but much health. High knock back and damage.
# Fox fast, but low health. High knock back but high damage.
# RACCOON slow, but high health. Normal knock back and little damage.

def random_enemy_type():
    return random.randint(0, 5)

class Enemy(Entity):
    def __init__(self, pos: list, enemy_type: int):
        super().__init__(pos[0], pos[1], 64, 64)

        self.__mOriginalSize: list = [64, 64]
        self.__mOriginalCollisionSize: list = [32, 35]

        #scenemanager.SCENE_MANAGER.get_current_scene().game_map().add_entity_to_check_collisions_for(self)

        self.__mEnemyType: int = enemy_type

        self.mTag = "ENEMY"
        self.mSpeed = self.__speed()
        self.__mDeathSpeed: float = 300

        self.mCollisionSize = [32, 35]

        self.__mAnimator: Animator = Animator(100, 7)
        self.__mAnimationToSet: str = "SPAWNING"

        self.__mSpawnIndicationAnimation: list = self.__spawn_indication_animation()
        self.__mIsSpawning: bool = True

        self.__set_up_animations()

        self.__mPlayerToFollow: Player = None

        self.__mMaxHealth: float = self.__max_health()
        self.__mCurrentHealth: float = self.__mMaxHealth
        self.__mIsDying: bool = False
        self.__mDeathBarrier: float = 300

        self.__mKnockBack: float = self.__knock_back()
        self.__mIsTakingKnockBack: bool = False
        self.__mMaxScaleMultiplier: float = 2
        self.__mCurrentScaleMultiplier: float = 50

        self.__mHealthBar: HealthBar = HealthBar(self.__mMaxHealth)

        self.__mDamage: int = self.__damage()


    def __spawn_indication_animation(self):
        indicators = os.listdir("resources/sprites/enemies/spawnindicator")

        m_indicator = random.choice(indicators)

        width: int = 96
        height: int = 96
        if m_indicator == "indicator02.png":
            height = 80

        return load_sprite_sheet(f"enemies/spawnindicator/{m_indicator}", width, height, None)

    def __set_up_animations(self):
        spriteSheet: list = load_sprite_sheet(self.__resource_path(), 32, 32, 52)

        self.__mAnimator.add_animation("DOWN_IDLE", get_sprites_from_index_A_to_index_B(0, 3, spriteSheet))

        self.__mAnimator.add_animation("DOWN_RUN", get_sprites_from_index_A_to_index_B(20, 27, spriteSheet))
        self.__mAnimator.add_animation("UP_RUN", get_sprites_from_index_A_to_index_B(44, 51, spriteSheet))
        self.__mAnimator.add_animation("RIGHT_RUN", get_sprites_from_index_A_to_index_B(36, 43, spriteSheet))
        self.__mAnimator.add_animation("LEFT_RUN", get_sprites_from_index_A_to_index_B(28, 35, spriteSheet))

        self.__mAnimator.add_animation("SPAWNING", self.__mSpawnIndicationAnimation, set_as_current_animation=True)

        self.__mAnimator.set_frame_rate_for_one_animation(400)

    def __knock_back(self) -> float:
        if self.__mEnemyType == BLUE_BIRD_ENEMY: return NORMAL_KNOCK_BACK
        elif self.__mEnemyType == WHITE_BIRD_ENEMY: return LITTLE_KNOCK_BACK
        elif self.__mEnemyType == GRAY_CAT_ENEMY: return LITTLE_KNOCK_BACK
        elif self.__mEnemyType == ORANGE_CAT_ENEMY: return HIGH_KNOCK_BACK
        elif self.__mEnemyType == FOX_ENEMY: return HIGH_KNOCK_BACK
        elif self.__mEnemyType == RACCOON_ENEMY: return NORMAL_KNOCK_BACK

    def __max_health(self) -> float:
        if self.__mEnemyType == BLUE_BIRD_ENEMY: return LOW_HEALTH
        elif self.__mEnemyType == WHITE_BIRD_ENEMY: return HIGH_HEALTH
        elif self.__mEnemyType == GRAY_CAT_ENEMY: return LOW_HEALTH
        elif self.__mEnemyType == ORANGE_CAT_ENEMY: return HIGH_HEALTH
        elif self.__mEnemyType == FOX_ENEMY: return LOW_HEALTH
        elif self.__mEnemyType == RACCOON_ENEMY: return HIGH_HEALTH

    def __speed(self) -> float:
        if self.__mEnemyType == BLUE_BIRD_ENEMY: return FAST_SPEED
        elif self.__mEnemyType == WHITE_BIRD_ENEMY: return SLOW_SPEED
        elif self.__mEnemyType == GRAY_CAT_ENEMY: return FAST_SPEED
        elif self.__mEnemyType == ORANGE_CAT_ENEMY: return FAST_SPEED
        elif self.__mEnemyType == FOX_ENEMY: return FAST_SPEED
        elif self.__mEnemyType == RACCOON_ENEMY: return SLOW_SPEED
        else:
            print(f"Invalid enemy type {self.__mEnemyType}")

    def __damage(self) -> int:
        if self.__mEnemyType == BLUE_BIRD_ENEMY: return LOW_DAMAGE
        elif self.__mEnemyType == WHITE_BIRD_ENEMY: return LOW_DAMAGE
        elif self.__mEnemyType == GRAY_CAT_ENEMY: return HIGH_DAMAGE
        elif self.__mEnemyType == ORANGE_CAT_ENEMY: return HIGH_DAMAGE
        elif self.__mEnemyType == FOX_ENEMY: return HIGH_DAMAGE
        elif self.__mEnemyType == RACCOON_ENEMY: return LOW_DAMAGE

    def __resource_path(self) -> str:
        path: str = "enemies/"

        if self.__mEnemyType == BLUE_BIRD_ENEMY: return path + "BIRDSPRITESHEET_Blue.png"
        elif self.__mEnemyType == WHITE_BIRD_ENEMY: return path + "BIRDSPRITESHEET_White.png"
        elif self.__mEnemyType == GRAY_CAT_ENEMY: return path + "CATSPRITESHEET_Gray.png"
        elif self.__mEnemyType == ORANGE_CAT_ENEMY: return path + "CATSPRITESHEET_Orange.png"
        elif self.__mEnemyType == FOX_ENEMY: return path + "FOXSPRITESHEET.png"
        elif self.__mEnemyType == RACCOON_ENEMY: return path + "RACCOONSPRITESHEET.png"

    def __handle_animations(self):

        if self.__mAnimator.current_animation_name() == "SPAWNING" and self.__mAnimator.is_last_frame():
            self.__mIsSpawning = False

        if self.mAcceleration.y < 0: #Moving up
            self.__mAnimationToSet = "UP_RUN"
        elif self.mAcceleration.y > 0:
            self.__mAnimationToSet = "DOWN_RUN"

        if self.mAcceleration.x > 0:
            self.__mAnimationToSet = "RIGHT_RUN"
        elif self.mAcceleration.x < 0:
            self.__mAnimationToSet = "LEFT_RUN"

        if self.__mIsSpawning:
            self.__mAnimationToSet = "SPAWNING"

        self.__mAnimator.set_current_animation(self.__mAnimationToSet)

    def __move(self):

        if self.mRect.x <= -self.__mDeathBarrier or self.mRect.x >= scenemanager.SCENE_MANAGER.get_current_scene().game_map().width() + self.__mDeathBarrier or self.mRect.y <= -self.__mDeathBarrier or self.mRect.y >= scenemanager.SCENE_MANAGER.get_current_scene().game_map().height() + self.__mDeathBarrier:
            scenemanager.SCENE_MANAGER.get_current_scene().remove_entity(self)

        if self.__mIsDying:
            self.mAcceleration.x = 0#random.randint(-1, 1)
            self.mAcceleration.y = 1
            self.mSpeed = self.__mDeathSpeed
            self.__mAnimator.stop()
            self.apply_acceleration()
            return

        if self.__mIsTakingKnockBack:
            return

        if self.__mIsSpawning:
            return

        dx: float = self.__mPlayerToFollow.mRect.x - self.mRect.x
        dy: float = self.__mPlayerToFollow.mRect.y - self.mRect.y

        dist: float = math.hypot(dx, dy)

        if dist == 0:
            return

        dx = dx/dist
        dy = dy/dist

        self.mAcceleration.x = dx
        self.mAcceleration.y = dy

    def __die(self):

        if not self.__mIsDying:
            soundmanager.SOUND_MANAGER.play_random_sound("death", soundmanager.SOUND_MANAGER.sound_effect_volume())
            scenemanager.SCENE_MANAGER.get_current_scene().level().increment_enemies_killed()
            scenemanager.SCENE_MANAGER.get_current_scene().level().check_for_level_finished()

        self.__mIsDying = True
        scenemanager.SCENE_MANAGER.get_current_scene().game_map().remove_entity_from_collisions(self)

    def __handle_scaling(self):
        if not self.__mIsTakingKnockBack:
            return

        self.mSize[0] += self.__mCurrentScaleMultiplier * gametime.DELTA_TIME
        self.mSize[1] += self.__mCurrentScaleMultiplier * gametime.DELTA_TIME

        self.mCollisionSize[0] += self.__mCurrentScaleMultiplier * gametime.DELTA_TIME
        self.mCollisionSize[1] += self.__mCurrentScaleMultiplier * gametime.DELTA_TIME

        if self.mSize[0] >= self.__mOriginalSize[0]*self.__mMaxScaleMultiplier:
            self.__mCurrentScaleMultiplier *= -1

        if self.mSize[0] <= self.__mOriginalSize[0]:
            self.__mIsTakingKnockBack = False
            self.__mCurrentScaleMultiplier *= -1
            self.__reset_sizes()

    def __health_bar_position(self) -> list:
        return [self.mRect.x - self.__mHealthBar.width()/4, self.mRect.y - self.mCollisionSize[1]]

    def __handle_player_collision(self):
        if not self.mRect.colliderect(self.__mPlayerToFollow.mRect):
            return

        if self.__mIsTakingKnockBack:
            return

        if self.__mIsSpawning:
            return

        self.__mPlayerToFollow.take_damage(self.__mDamage)

    def take_damage(self, amount: float):

        if not self.__mIsTakingKnockBack:
            soundmanager.SOUND_MANAGER.play_random_sound("enemyhit", soundmanager.SOUND_MANAGER.sound_effect_volume())

        self.__mCurrentHealth -= amount
        self.__mIsTakingKnockBack = True


        self.mAcceleration.x = -self.mAcceleration.x * self.__mKnockBack
        self.mAcceleration.y = -self.mAcceleration.y * self.__mKnockBack

        if self.__mCurrentHealth <= 0:
            self.__mCurrentHealth = 0
            self.__die()

    def on_collision_with_tile(self):
        super().on_collision_with_tile()
        if self.__mIsTakingKnockBack:
            self.mAcceleration.x *= -1
            self.mAcceleration.y *= -1

    def __reset_sizes(self):
        self.mSize[0] = self.__mOriginalSize[0]
        self.mSize[1] = self.__mOriginalSize[1]
        self.mCollisionSize[0] = self.__mOriginalCollisionSize[0]
        self.mCollisionSize[1] = self.__mOriginalCollisionSize[1]

    def update(self):
        super().update()

        if self.__mPlayerToFollow == None: self.__mPlayerToFollow = scenemanager.SCENE_MANAGER.get_current_scene().get_entity_with_tag("PLAYER")

        self.__move()
        self.__handle_scaling()
        self.__handle_animations()

        self.mRect.w = self.mCollisionSize[0]
        self.mRect.h = self.mCollisionSize[1]

        self.__handle_player_collision()

        self.__mAnimator.update_animations()

    def render(self):
        super().render()
        renderer.RENDERER.draw_sprite(self.__mAnimator.get_current_frame(), (self.mRect.x - self.mSize[0]/4, self.mRect.y - self.mSize[1]/4), self.mSize)
        self.__mHealthBar.render(self.__mCurrentHealth, self.__health_bar_position())
        #super()._render_rect()



class HealthBar:
    def __init__(self, max_health: float):

        self.__mMaxHealth: float = max_health

        self.__mSize: tuple = (108, 10)

        self.__mFrame: pygame.Surface = load_image("resources/sprites/enemies/healthbar/EnemyHealthBarFrame.png", self.__mSize)
        self.__mFilling: pygame.Surface = load_image("resources/sprites/enemies/healthbar/EnemyHealthBarFilling.png", self.__mSize)

    def render(self, current_health: float, position: list):
        renderer.RENDERER.draw_sprite(self.__mFrame, position, self.__mSize)
        if current_health > 0:
            renderer.RENDERER.draw_sprite(self.__mFilling, (position[0] + 8, position[1]), (self.__filling_width(current_health), self.__mSize[1]))

    def width(self) -> float: return self.__mSize[0]

    def height(self) -> float: return self.__mSize[1]

    def __filling_width(self, current_health: float):
        return max((current_health/self.__mMaxHealth) * self.__mSize[0] - 8, 0)