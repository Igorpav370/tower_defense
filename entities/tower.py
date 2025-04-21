import pygame
import math
from config import TILE_SIZE, TOWER_ANGLE_OFFSET
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
        self.nearest = None
        self.last_angle = -90
        self.rotation_speed = 2.0  # градусов за кадр
        self.current_angle = -90   # начальный угол (плавный)

    def update(self, enemies, bullets):
        self.nearest = None
        min_dist = float("inf")
        self.timer += 1

        for enemy in enemies:
            dx = enemy.x - self.x
            dy = enemy.y - self.y
            distance = math.hypot(dx, dy)
            if distance < min_dist:
                min_dist = distance
                self.nearest = enemy

        if self.timer >= self.cooldown:
            if self.nearest:
                dx = self.nearest.x - self.x
                dy = self.nearest.y - self.y
                distance = math.hypot(dx, dy)
                if distance <= self.range:
                    desired = math.degrees(math.atan2(-dy, dx)) + TOWER_ANGLE_OFFSET
                    desired = (desired + 360) % 360
                    current = (self.current_angle + 360) % 360
                    diff = (desired - current + 540) % 360 - 180
                    if abs(diff) < 5:  # башня навелась
                        bullets.append(Bullet(
                            x=self.x + TILE_SIZE//2,
                            y=self.y + TILE_SIZE//2,
                            target=self.nearest,
                            img=self.bullet_img
                        ))
                        self.timer = 0


    def draw(self, surface):
        target_angle = self.current_angle

        if self.nearest:
            dx = self.nearest.x - self.x
            dy = self.nearest.y - self.y
            desired = math.degrees(math.atan2(-dy, dx)) + TOWER_ANGLE_OFFSET
            desired = (desired + 360) % 360
            current = (self.current_angle + 360) % 360

            diff = (desired - current + 540) % 360 - 180  # кратчайший путь

            if abs(diff) < self.rotation_speed:
                self.current_angle = desired
            else:
                self.current_angle += self.rotation_speed * (1 if diff > 0 else -1)

            self.current_angle %= 360  # держим в пределах круга
        
        rotated = pygame.transform.rotate(self.image, self.current_angle)
        rect = rotated.get_rect(center=(self.x + TILE_SIZE//2, self.y + TILE_SIZE//2))
        surface.blit(rotated, rect.topleft)
        
        pygame.draw.circle(surface, (0, 0, 255),
                         (self.x + TILE_SIZE//2, self.y + TILE_SIZE//2),
                         self.range, 1)