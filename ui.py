import pygame
from config import *
from game import get_current_wave_number

font = pygame.font.SysFont("arial", 24)

def draw_ui(surface, money, base_health):
    money_text = font.render(f"Money: {money}", True, (0, 0, 0))
    health_text = font.render(f"Base HP: {base_health}", True, (200, 0, 0))
    wave_text = font.render(f"Wave: {get_current_wave_number()}", True, (0, 0, 0))
    surface.blit(wave_text, (10, 70))
    surface.blit(money_text, (10, 10))
    surface.blit(health_text, (10, 40))

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
