import pygame
import math

class Bullet:
    def __init__(self, x, y, target, img=None):
        self.x = x
        self.y = y
        self.target = target
        self.speed = 5
        self.image = img
        self.damage = 1

    def update(self):
        if not self.target or getattr(self.target, "health", 0) <= 0:
            return False

        dx = self.target.x - self.x
        dy = self.target.y - self.y
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