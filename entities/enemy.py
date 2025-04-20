import pygame
import math
from config import TILE_SIZE


class Enemy:
    def __init__(self, path, img, health=3, speed=2):
        self.path = path
        self.current_point = 0
        self.x, self.y = path[0]
        self.speed = speed
        self.health = health
        self.image = img
        self.reached_end = False
        self.target_angle = 0
        self.current_angle = 0

    def update(self):
        if self.current_point < len(self.path) - 1:
            target_x, target_y = self.path[self.current_point + 1]

            # Вычисляем вектор направления
            dx = target_x - self.x
            dy = target_y - self.y


            # Рассчитываем угол в радианах, затем конвертируем в градусы
            self.target_angle = math.degrees(math.atan2(-dy, dx)) % 360

            # Движение остаётся прежним
            dist = math.hypot(dx, dy)
            if dist < self.speed:
                self.x, self.y = target_x, target_y
                self.current_point += 1
            else:
                self.x += self.speed * dx / dist
                self.y += self.speed * dy / dist
            return False
        else:
            if not self.reached_end:
                self.reached_end = True
                return True
            return False

    def draw(self, surface):
        # Поворачиваем изображение
        angle_diff = (self.target_angle - self.current_angle + 180) % 360 - 180
        self.current_angle += angle_diff * 0.1  # Коэффициент плавности
        rotated_image = pygame.transform.rotozoom(self.image, self.current_angle, 1)

        # Центрируем повёрнутое изображение
        rect = rotated_image.get_rect(center=(self.x + TILE_SIZE // 2, self.y + TILE_SIZE // 2))
        surface.blit(rotated_image, rect.topleft)