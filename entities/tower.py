import pygame
import math
from config import TILE_SIZE
from entities.bullet import Bullet

class Tower:
    def __init__(self, x, y, img, bullet_img):
        self.x = x
        self.y = y
        self.range = 100
        self.cooldown = 60
        self.timer = 0
        self.image = img
        self.bullet_img = bullet_img

    def update(self, enemies, bullets):
        self.timer += 1
        if self.timer >= self.cooldown:
            for enemy in enemies:
                dx = enemy.x - self.x
                dy = enemy.y - self.y
                distance = math.hypot(dx, dy)
                if distance <= self.range:
                    bullets.append(Bullet(
                        self.x + TILE_SIZE//2,
                        self.y + TILE_SIZE//2,
                        enemy,
                        self.bullet_img
                    ))
                    self.timer = 0
                    break

    def draw(self, surface, enemies):
        nearest = None
        min_dist = float("inf")
        for enemy in enemies:
            dx = enemy.x - self.x
            dy = enemy.y - self.y
            dist = math.hypot(dx, dy)
            if dist < min_dist:
                min_dist = dist
                nearest = enemy

        if nearest:
            angle = math.degrees(math.atan2(-(nearest.y - self.y), nearest.x - self.x))
            rotated = pygame.transform.rotate(self.image, angle)
            rect = rotated.get_rect(center=(self.x + TILE_SIZE//2, self.y + TILE_SIZE//2))
            surface.blit(rotated, rect.topleft)
        else:
            surface.blit(self.image, (self.x, self.y))

        pygame.draw.circle(surface, (0, 0, 255),
                         (self.x + TILE_SIZE//2, self.y + TILE_SIZE//2),
                         self.range, 1)