import pygame
from config import *
from game import *

font = pygame.font.SysFont("arial", 24)

def draw_ui(surface, money, base_health, selected_tower_type):
    money_text = font.render(f"Money: {money}", True, (0, 0, 0))
    health_text = font.render(f"Base HP: {base_health}", True, (200, 0, 0))
    wave_text = font.render(f"Wave: {get_current_wave_number()}", True, (0, 0, 0))
    left_text = font.render(f"Enemies left: {get_enemies_left()}", True, (0, 0, 0))
    
    surface.blit(money_text, (10, 10))
    surface.blit(health_text, (10, 40))
    surface.blit(wave_text, (10, 70))
    surface.blit(left_text, (10, 100))

    for i, (tower_type, tower_img) in enumerate(tower_images.items()):
        tower_x = 10 + i * (40 + 40)
        tower_y = 540
        
        tower_class = tower_classes[tower_type]
        tower_image = tower_images.get(tower_type)
        temp_tower = tower_class(-1000, -1000, tower_image)
        
        if tower_type in tower_images:
            scaled_img = pygame.transform.scale(tower_images[tower_type], (40, 40))
            surface.blit(scaled_img, (tower_x, tower_y))
        
        name_text = font.render(tower_type.capitalize(), True, (0, 0, 0))
        cost_text = font.render(f"${temp_tower.cost}", True, (0, 100, 0))
        
        name_x = tower_x + (40 - name_text.get_width()) // 2
        cost_x = tower_x + (40 - cost_text.get_width()) // 2
        
        surface.blit(name_text, (name_x, tower_y + 40 + 5))
        surface.blit(cost_text, (cost_x, tower_y + 40 + 25))
        
        if money < temp_tower.cost:
            s = pygame.Surface((50, 50), pygame.SRCALPHA)
            s.fill((100, 100, 100, 150))
            surface.blit(s, (tower_x - 5, tower_y - 5))

        is_selected = tower_type == selected_tower_type
        if is_selected:
            pygame.draw.rect(surface, (0, 255, 0), 
                           (tower_x - 5, tower_y - 5, 
                            40 + 10, 40 + 10), 
                           2)

    if base_health <= 0:
        game_over_text = font.render("GAME OVER", True, (255, 0, 0))
        surface.blit(game_over_text, (WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2))


def draw_game_over(surface):
    surface.fill(WHITE)
    font_big = pygame.font.SysFont("arial", 48, bold=True)
    font_small = pygame.font.SysFont("arial", 32)

    game_over_text = font_big.render("GAME OVER", True, (255, 0, 0))
    retry_text = font_small.render("Заново", True, (0, 0, 0))
    quit_text = font_small.render("Выход", True, (0, 0, 0))

    surface.blit(game_over_text, (WINDOW_WIDTH // 2 - game_over_text.get_width() // 2, 200))

    retry_rect = pygame.Rect(WINDOW_WIDTH // 2 - 100, 300, 200, 50)
    quit_rect = pygame.Rect(WINDOW_WIDTH // 2 - 100, 370, 200, 50)

    pygame.draw.rect(surface, (200, 200, 200), retry_rect)
    pygame.draw.rect(surface, (200, 200, 200), quit_rect)

    surface.blit(retry_text, (retry_rect.x + 60, retry_rect.y + 10))
    surface.blit(quit_text, (quit_rect.x + 70, quit_rect.y + 10))

    return retry_rect, quit_rect


def draw_game_win(surface):
    surface.fill(WHITE)
    font_big = pygame.font.SysFont("arial", 48, bold=True)
    font_small = pygame.font.SysFont("arial", 32)

    game_win_text = font_big.render("GAME WIN", True, (0, 255, 0))
    retry_text = font_small.render("Заново", True, (0, 0, 0))
    quit_text = font_small.render("Выход", True, (0, 0, 0))

    surface.blit(game_win_text, (WINDOW_WIDTH // 2 - game_win_text.get_width() // 2, 200))

    retry_rect = pygame.Rect(WINDOW_WIDTH // 2 - 100, 300, 200, 50)
    quit_rect = pygame.Rect(WINDOW_WIDTH // 2 - 100, 370, 200, 50)

    pygame.draw.rect(surface, (200, 200, 200), retry_rect)
    pygame.draw.rect(surface, (200, 200, 200), quit_rect)

    surface.blit(retry_text, (retry_rect.x + 60, retry_rect.y + 10))
    surface.blit(quit_text, (quit_rect.x + 70, quit_rect.y + 10))

    return retry_rect, quit_rect

def draw_tower_menu(surface, menu_pos):
    tx, ty = menu_pos
    for i, tower_type in enumerate(tower_classes.keys()):
        rect = pygame.Rect(tx, ty + i * 40, 150, 35)
        pygame.draw.rect(surface, (50, 50, 50), rect)
        pygame.draw.rect(surface, (200, 200, 200), rect, 2)

        tower_class = tower_classes[tower_type]
        temp_tower = tower_class(-1000, -1000)

        font = pygame.font.SysFont(None, 24)
        label = font.render(f"{tower_type.capitalize()} - {temp_tower.cost}", True, (255, 255, 255))
        surface.blit(label, (rect.x + 10, rect.y + 8))
