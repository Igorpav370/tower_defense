import pygame
import math
from config import TILE_SIZE


class BaseBullet:
    def __init__(self, x, y, target, img=None):
        self.x = x
        self.y = y
        self.target = target
        self.image = img
        self.speed = 5
        self.damage = 1

    def update(self):
        if not self.target or getattr(self.target, "health", 0) <= 0:
            return False

        dx = (self.target.x + TILE_SIZE // 2) - self.x
        dy = (self.target.y + TILE_SIZE // 2) - self.y
        dist = math.hypot(dx, dy)

        if dist < self.speed:
            self.target.health -= self.damage
            return False

        self.x += self.speed * dx / dist
        self.y += self.speed * dy / dist
        return True

    def draw(self, surface):
        if self.image:
            rect = self.image.get_rect(center=(int(self.x), int(self.y)))
            surface.blit(self.image, rect)
        else:
            pygame.draw.circle(surface, (255, 0, 0), (int(self.x), int(self.y)), 5)


class BasicBullet(BaseBullet):
    def __init__(self, x, y, target, img=None):
        super().__init__(x, y, target, img)
        self.speed = 6
        self.damage = 1

class AdvancedBullet(BaseBullet):
    def __init__(self, x, y, target, img=None):
        super().__init__(x, y, target, img)
        self.speed = 6
        self.damage = 2
