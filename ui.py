import pygame
from config import *

font = pygame.font.SysFont("arial", 24)

def draw_ui(surface, money, base_health):
    money_text = font.render(f"Money: {money}", True, (0, 0, 0))
    health_text = font.render(f"Base HP: {base_health}", True, (200, 0, 0))
    surface.blit(money_text, (10, 10))
    surface.blit(health_text, (10, 40))

    if base_health <= 0:
        game_over_text = font.render("GAME OVER", True, (255, 0, 0))
        surface.blit(game_over_text, (WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2))
