import pygame

import renderer

class Entity:
    def __init__(self, x: float, y: float, w: float, h: float):
        self.mCollisionSize: list = [w, h]
        self.mSize: list = [w, h]
        self.mAcceleration: pygame.Vector2 = pygame.Vector2(0, 0)
        self.mRect: pygame.Rect = pygame.Rect(x, y, w, h)

        self.mTag: str = ""

        self.mSpeed: float = 0.0


    def update(self):
        pass

    def render(self): pass

    def get_rect(self) -> pygame.Rect: return self.mRect

    def _render_rect(self):
        renderer.RENDERER.draw_rect(self.mRect, (255, 0, 0), size=1)

    def on_collision_with_tile(self): pass

    def apply_acceleration(self):
        self.mRect.x += self.mAcceleration.x * self.mSpeed
        self.mRect.y += self.mAcceleration.y * self.mSpeed

