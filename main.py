import pygame

pygame.init()
window = pygame.display.set_mode((640, 640))  # Используйте WINDOW_WIDTH и WINDOW_HEIGHT из config.py
pygame.display.set_caption("Tower Defense")
clock = pygame.time.Clock()

from game import *
from config import *
from ui import draw_ui, draw_game_over, draw_tower_menu, draw_game_win

# Для меню выбора башни
tower_menu_visible = False
tower_menu_pos = (0, 0)
selected_tower_type = None

def game_over_screen():
    if get_base_health() > 0:
        return False
    while True:
        retry_rect, quit_rect = draw_game_over(window)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if retry_rect.collidepoint(event.pos):
                    return True  # Перезапустить
                elif quit_rect.collidepoint(event.pos):
                    pygame.quit()
                    exit()


def game_win_screen():
    if not get_win_status():
        return False
    while True:
        retry_rect, quit_rect = draw_game_win(window)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if retry_rect.collidepoint(event.pos):
                    return True  # Перезапустить
                elif quit_rect.collidepoint(event.pos):
                    pygame.quit()
                    exit()


# Функция для обработки клика по меню башен
def handle_tower_menu_click(mx, my):
    global selected_tower_type, tower_menu_visible
    tx, ty = tower_menu_pos

    for i, tower_type in enumerate(tower_classes.keys()):
        button_rect = pygame.Rect(tx, ty + i * 40, 100, 35)
        if button_rect.collidepoint(mx, my):
            selected_tower_type = tower_type
            tower_menu_visible = False
            break
    tower_menu_visible = False

# Основной игровой цикл
running = True
while running:
    clock.tick(FPS)

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:  # Правая кнопка мыши
                tower_menu_visible = True
                tower_menu_pos = event.pos
            elif event.button == 1:  # Левая кнопка мыши
                if tower_menu_visible:
                    mx, my = event.pos
                    handle_tower_menu_click(mx, my)
                elif selected_tower_type:
                    # Установка башни с выбранным типом
                    place_tower(event.pos, selected_tower_type)

    # Обновление игры
    enemies = update_game()

    # Отображение
    window.fill(WHITE)

    # Отрисовка карты
    for y, row in enumerate(tilemap):
        for x, tile in enumerate(row):
            img = tileset.get(tile, tileset[" "])
            window.blit(img, (x * TILE_SIZE, y * TILE_SIZE))

    # Отрисовка объектов
    for tower in towers:
        tower.draw(window)

    for bullet in bullets:
        bullet.draw(window)

    for enemy in enemies:
        enemy.draw(window)

    # Отрисовка UI
    draw_ui(window, get_money(), get_base_health(), selected_tower_type)

    # Отрисовка контекстного меню башен
    if tower_menu_visible:
        draw_tower_menu(window, tower_menu_pos)

    pygame.display.flip()

    if game_over_screen() or game_win_screen():
        reset_game()
        towers.clear()
        bullets.clear()
        enemies.clear()

pygame.quit()
