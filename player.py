import pygame

from entity import Entity
from gameinput import *
from spritesheetloader import load_sprite_sheet
from animator import Animator
from heart import Heart
import renderer
import camera
import scenemanager
import soundmanager

# Character sprites: https://szadiart.itch.io/rpg-main-character
# World sprites: https://szadiart.itch.io/rpg-worlds-ca
# Enemies: https://pixelfight.itch.io/birdcat
# Health bar: https://adwitr.itch.io/pixel-health-bar-asset-pack-2
# Font: https://poppyworks.itch.io/silver
# Keyboard icons: https://dreammix.itch.io/keyboard-keys-for-ui
# More map stuff: https://szadiart.itch.io/rogue-fantasy-catacombs
# FBX: https://ragnapixel.itch.io/particle-fx
# Sound effects: https://sfxr.me/
# Panel: https://evan-p.itch.io/pixel-ui-template
# Map render order: right down (0, 0) -> (1, 1) ?

class Player(Entity):
    def __init__(self, pos: list):
        super().__init__(pos[0], pos[1], 96, 96)

        #scenemanager.SCENE_MANAGER.get_current_scene().game_map().add_entity_to_check_collisions_for(self)

        self.mSpeed = 3
        self.mTag = "PLAYER"
        self.mCollisionSize = [24, 48]

        self.mRect.w = self.mCollisionSize[0]
        self.mRect.h = self.mCollisionSize[1]

        self.__mLastAcceleration: list = [1, 1] #Axis (0=x, 1=y), value

        self.__mJustAttacked: bool = False
        self.__mIsAttacking: bool = False
        self.__mFacingRight: bool = False

        self.__mAttackHitBoxOffset: list = [50, 50]
        self.__mAttackHitBoxSize: float = 20

        self.__mDamage: float = 1
        self.__mDamageTimer: float = 40
        self.__mCurrentDamageTime: float = 0.0
        self.__mTakingDamage: bool = False
        self.__mDied: bool = False

        self.__mMaxHearts: int = 6
        self.__mCurrentHearts: int = self.__mMaxHearts
        self.__mHearts: list = []
        self.__mHeartsStartPos: list = [170, 17]
        self.__mHeartOffset: int = 20
        self.__generate_hearts()

        self.__mGivenUp: bool = False

        self.__mAnimator: Animator = Animator(1, 7)
        self.__mAnimationToSet: str = ""
        self.__set_up_animations()

    def __set_up_animations(self):
        self.__mAnimator.add_animation("DOWN_IDLE", load_sprite_sheet("player/_down idle.png", 64, 64, 5), set_as_current_animation=True)
        self.__mAnimator.add_animation("UP_IDLE", load_sprite_sheet("player/_up idle.png", 64, 64, 5))
        self.__mAnimator.add_animation("LEFT_IDLE", load_sprite_sheet("player/_side idle.png", 64, 64, 5))
        self.__mAnimator.add_animation("RIGHT_IDLE", load_sprite_sheet("player/_side idle.png", 64, 64, 5, flip_frames_horizontally=True))

        self.__mAnimator.add_animation("UP_WALK", load_sprite_sheet("player/_up walk.png", 64, 64, 6))
        self.__mAnimator.add_animation("DOWN_WALK", load_sprite_sheet("player/_down walk.png", 64, 64, 6))
        self.__mAnimator.add_animation("LEFT_WALK", load_sprite_sheet("player/_side walk.png", 64, 64, 6))
        self.__mAnimator.add_animation("RIGHT_WALK", load_sprite_sheet("player/_side walk.png", 64, 64, 6, flip_frames_horizontally=True))

        self.__mAnimator.add_animation("DOWN_ATTACK", load_sprite_sheet("player/_down attack.png", 64, 64, 3))
        self.__mAnimator.add_animation("UP_ATTACK", load_sprite_sheet("player/_up attack.png", 64, 64, 3))
        self.__mAnimator.add_animation("LEFT_ATTACK", load_sprite_sheet("player/_side attack.png", 64, 64, 3))
        self.__mAnimator.add_animation("RIGHT_ATTACK", load_sprite_sheet("player/_side attack.png", 64, 64, 3, flip_frames_horizontally=True))

    def __move(self):
        if GAME_INPUT.keyboard_key_pressed(UP_KEY):
            self.mAcceleration.y = -1
            if not self.__mIsAttacking:
                self.__mAnimationToSet = "UP_WALK"
            self.__mLastAcceleration = [1, -1]

        if GAME_INPUT.keyboard_key_pressed(DOWN_KEY):
            self.mAcceleration.y = 1
            if not self.__mIsAttacking:
                self.__mAnimationToSet = "DOWN_WALK"
            self.__mLastAcceleration = [1, 1]

        if GAME_INPUT.keyboard_key_pressed(LEFT_KEY):
            self.mAcceleration.x = -1
            if not self.__mIsAttacking:
                self.__mAnimationToSet = "LEFT_WALK"
            self.__mLastAcceleration = [0, -1]
            self.__mFacingRight = False

        if GAME_INPUT.keyboard_key_pressed(RIGHT_KEY):
            self.mAcceleration.x = 1
            if not self.__mIsAttacking:
                self.__mAnimationToSet = "RIGHT_WALK"
            self.__mLastAcceleration = [0, 1]
            self.__mFacingRight = True

        if self.mAcceleration.x != 0 and self.mAcceleration.y != 0:
            self.mAcceleration = self.mAcceleration.normalize()

        if not GAME_INPUT.keyboard_key_pressed(UP_KEY) and not GAME_INPUT.keyboard_key_pressed(DOWN_KEY):
            self.mAcceleration.y = 0

        if not GAME_INPUT.keyboard_key_pressed(LEFT_KEY) and not GAME_INPUT.keyboard_key_pressed(RIGHT_KEY):
            self.mAcceleration.x = 0

        if self.mAcceleration.x == 0 and self.mAcceleration.y == 0:
            if "ATTACK" not in self.__mAnimationToSet:
                self.__set_idle_animation()

    def __handle_attacking(self):
        if GAME_INPUT.keyboard_key_pressed(ATTACK_KEY) and not self.__mJustAttacked and "ATTACK" not in self.__mAnimator.current_animation_name():
            self.__mJustAttacked = True
            self.__mIsAttacking = True

            if "UP" in self.__mAnimationToSet: self.__mAnimationToSet = "UP_ATTACK"
            if "DOWN" in self.__mAnimationToSet: self.__mAnimationToSet = "DOWN_ATTACK"
            if "RIGHT" in self.__mAnimationToSet: self.__mAnimationToSet = "RIGHT_ATTACK"
            if "LEFT" in self.__mAnimationToSet: self.__mAnimationToSet = "LEFT_ATTACK"

            self.mAcceleration.x = 0
            self.mAcceleration.y = 0

            self.__mAnimator.set_frame_rate_for_one_animation(0.8)

            self.__attack()

        if not GAME_INPUT.keyboard_key_pressed(ATTACK_KEY):
            self.__mJustAttacked = False

        if "ATTACK" in self.__mAnimator.current_animation_name() and self.__mAnimator.is_last_frame():
            #self.__mAnimationToSet = "DOWN_IDLE"
            self.__set_idle_animation()
            self.__mIsAttacking = False

    def __set_idle_animation(self):
        if self.__mLastAcceleration[0] == 0:
            if self.__mLastAcceleration[1] == -1:
                self.__mAnimationToSet = "LEFT_IDLE"
            elif self.__mLastAcceleration[1] == 1:
                self.__mAnimationToSet = "RIGHT_IDLE"
        elif self.__mLastAcceleration[0] == 1:
            if self.__mLastAcceleration[1] == -1:
                self.__mAnimationToSet = "UP_IDLE"
            elif self.__mLastAcceleration[1] == 1:
                self.__mAnimationToSet = "DOWN_IDLE"

    def __attack(self):
        mAttackHitBox: pygame.Rect = self.__attack_hit_box()
        enemyEntities: list = scenemanager.SCENE_MANAGER.get_current_scene().enemy_entities()

        for enemy in enemyEntities:
            if mAttackHitBox.colliderect(enemy.get_rect()):
                enemy.take_damage(self.__mDamage)

    def __attack_hit_box(self) -> pygame.Rect:
        default_x: float = self.mRect.centerx
        default_y: float = self.mRect.centery

        if "UP" in self.__mAnimationToSet:
            return pygame.Rect(default_x - self.__mAttackHitBoxSize/2, default_y - self.__mAttackHitBoxOffset[1] - self.mCollisionSize[1]/2, self.__mAttackHitBoxSize, self.__mAttackHitBoxOffset[1])
        elif "DOWN" in self.__mAnimationToSet:
            return pygame.Rect(default_x - self.__mAttackHitBoxSize/2, default_y + self.mCollisionSize[1]/2, self.__mAttackHitBoxSize, self.__mAttackHitBoxOffset[1])
        elif "RIGHT" in self.__mAnimationToSet:
            return pygame.Rect(default_x + self.mCollisionSize[0]/2, default_y - self.__mAttackHitBoxSize/2, self.__mAttackHitBoxOffset[0], self.__mAttackHitBoxSize)
        elif "LEFT" in self.__mAnimationToSet:
            return pygame.Rect(default_x - self.mCollisionSize[0]/2 - self.__mAttackHitBoxOffset[0], default_y - self.__mAttackHitBoxSize/2, self.__mAttackHitBoxOffset[0], self.__mAttackHitBoxSize)
        else:
            return pygame.Rect(default_x, default_y, self.__mAttackHitBoxSize, self.__mAttackHitBoxSize)

    def __generate_hearts(self):
        for i in range(0, self.__mMaxHearts):
            self.__mHearts.append(Heart())

    def __render_hearts(self):
        renderer.RENDERER.draw_text("Current Hearts: ", (10, 10))
        for i in range(0, len(self.__mHearts)):
            filling = True if i+1 <= self.__mCurrentHearts else False
            self.__mHearts[i].render(filling, [self.__mHeartsStartPos[0] + i*self.__mHeartOffset, self.__mHeartsStartPos[1]])

    def __handle_damage_timer(self):
        if not self.__mTakingDamage:
            return

        self.__mCurrentDamageTime += 1
        if self.__mCurrentDamageTime >= self.__mDamageTimer:
            self.__mTakingDamage = False
            self.__mCurrentDamageTime = 0.0

    def __die(self):
        self.__mDied = True
        soundmanager.SOUND_MANAGER.play_random_sound("playerdeath", soundmanager.SOUND_MANAGER.sound_effect_volume())

    def take_damage(self, damage: int):
        if not self.__mTakingDamage:
            self.__mCurrentHearts -= damage
            self.__mTakingDamage = True

            soundmanager.SOUND_MANAGER.play_random_sound("playerhit", soundmanager.SOUND_MANAGER.sound_effect_volume())

        if self.__mCurrentHearts <= 0 and not self.__mDied:
            self.__die()

    def current_hearts(self) -> int: return self.__mCurrentHearts

    def is_dead(self) -> bool: return self.__mDied

    def __handle_giving_up(self):
        if GAME_INPUT.keyboard_key_pressed(GIVE_UP_KEY):
            self.__mGivenUp = True

    def given_up(self): return self.__mGivenUp

    def update(self):
        super().update()

        self.__handle_giving_up()
        self.__move()
        self.__handle_attacking()
        self.__mAnimator.set_current_animation(self.__mAnimationToSet)
        self.__mAnimator.update_animations()
        self.__handle_damage_timer()


        camera.CAMERA.follow_player((self.mRect.x, self.mRect.y))

    def render(self):
        super().render()
        renderer.RENDERER.draw_sprite(self.__mAnimator.get_current_frame(), [self.mRect.x - self.mSize[0]/2 + self.mCollisionSize[0]/2, self.mRect.y - self.mSize[1]/2 + self.mCollisionSize[1]/2], self.mSize)
        self.__render_hearts()
        #renderer.RENDERER.draw_rect(self.__attack_hit_box(), (255, 0, 0), size=1)
        #super()._render_rect()
