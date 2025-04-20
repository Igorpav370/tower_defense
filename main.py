# main.py
import pygame


# Инициализация Pygame и создание окна
pygame.init()
window = pygame.display.set_mode((640, 640))  # Используйте WINDOW_WIDTH и WINDOW_HEIGHT из config.py
pygame.display.set_caption("Tower Defense")
clock = pygame.time.Clock()


# Теперь можно импортировать модули, которые используют pygame
from game import *
from config import *
from ui import draw_ui

# Основной игровой цикл
running = True
while running:
    clock.tick(FPS)

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            grid_x = mx // TILE_SIZE
            grid_y = my // TILE_SIZE
            place_tower((grid_x * TILE_SIZE, grid_y * TILE_SIZE))

    # Обновление игры
    enemies = update_game()

    # Отображение
    window.fill(WHITE)

    # Отрисовка карты
    for y, row in enumerate(tilemap):
        for x, tile in enumerate(row):
            img = tileset.get(tile, tileset["G"])
            window.blit(img, (x * TILE_SIZE, y * TILE_SIZE))

    # Отрисовка объектов
    for tower in towers:
        tower.draw(window, enemies)

    for bullet in bullets:
        bullet.draw(window)

    for enemy in enemies:
        enemy.draw(window)

    draw_ui(window, get_money(), get_base_health())


    pygame.display.flip()

    # Если здоровье базы 0, выводим GAME OVER
    if get_base_health() <= 0:
        draw_ui(window, get_money(), get_base_health())
        pygame.display.flip()
        pygame.time.delay(3000)
        running = False

pygame.quit()