import pygame
import math
from config import TILE_SIZE, TOWER_ANGLE_OFFSET
from entities.bullet import BasicBullet, AdvancedBullet


class BaseTower:
    def __init__(self, x, y, image, bullet_class=BasicBullet, bullet_img=None, cost=50):
        self.x = x
        self.y = y
        self.image = image
        self.range = 100
        self.cooldown = 60
        self.timer = 0
        self.bullet_img = bullet_img
        self.bullet_class = bullet_class
        self.rotation_speed = 2.0
        self.current_angle = -90
        self.nearest = None
        self.cost = cost

    def update(self, enemies, bullets):
        self.timer += 1
        self.nearest = None
        min_dist = float("inf")

        for enemy in enemies:
            dx = enemy.x - self.x
            dy = enemy.y - self.y
            distance = math.hypot(dx, dy)
            if distance < min_dist:
                min_dist = distance
                self.nearest = enemy

        if self.timer >= self.cooldown and self.nearest and min_dist <= self.range:
            # Башня повернулась достаточно, чтобы стрелять
            dx = self.nearest.x - self.x
            dy = self.nearest.y - self.y
            angle_to_target = math.degrees(math.atan2(-dy, dx)) + TOWER_ANGLE_OFFSET
            angle_to_target = (angle_to_target + 360) % 360
            current = (self.current_angle + 360) % 360
            diff = (angle_to_target - current + 540) % 360 - 180
            if abs(diff) < 5:
                bullet = self.bullet_class(
                    x=self.x + TILE_SIZE // 2,
                    y=self.y + TILE_SIZE // 2,
                    target=self.nearest,
                    img=self.bullet_img
                )
                bullets.append(bullet)
                self.timer = 0

    def draw(self, surface):
        if self.nearest:
            dx = self.nearest.x - self.x
            dy = self.nearest.y - self.y
            desired = math.degrees(math.atan2(-dy, dx)) + TOWER_ANGLE_OFFSET
            desired = (desired + 360) % 360
            current = (self.current_angle + 360) % 360
            diff = (desired - current + 540) % 360 - 180
            if abs(diff) < self.rotation_speed:
                self.current_angle = desired
            else:
                self.current_angle += self.rotation_speed * (1 if diff > 0 else -1)
                self.current_angle %= 360

        rotated = pygame.transform.rotate(self.image, self.current_angle)
        rect = rotated.get_rect(center=(self.x + TILE_SIZE // 2, self.y + TILE_SIZE // 2))
        surface.blit(rotated, rect.topleft)

        pygame.draw.circle(surface, (0, 0, 255),
                           (self.x + TILE_SIZE // 2, self.y + TILE_SIZE // 2),
                           self.range, 1)


class BasicTower(BaseTower):
    def __init__(self, x, y, image, bullet_img):
        super().__init__(x, y, image, bullet_class=BasicBullet, bullet_img=bullet_img)
        self.range = 100
        self.cooldown = 60
        self.cost = 50

class AdvancedTower(BaseTower):
    def __init__(self, x, y, image, bullet_img):
        super().__init__(x, y, image, bullet_class=AdvancedBullet, bullet_img=bullet_img)
        self.range = 100
        self.cooldown = 60
        self.cost = 100
