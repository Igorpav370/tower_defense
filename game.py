import pygame
import json
from entities.enemy import Enemy
from entities.tower import Tower
from entities.bullet import Bullet
from config import *
from pathlib import Path

# === Загрузка ресурсов ===
assets_dir = Path("assets")
tileset = {
    "G": pygame.image.load(assets_dir / "tiles" / "grass.png"),
    "P": pygame.image.load(assets_dir / "tiles" / "path.png")
}
enemy_img = pygame.image.load(assets_dir / "enemies" / "basic_enemy2.png")
tower_img = pygame.image.load(assets_dir / "towers" / "basic_tower.png")
bullet_img = pygame.image.load(assets_dir / "towers" / "bullet.png").convert_alpha()

# === Загрузка карты ===
with open("levels/level1.json", "r") as f:
    level_data = json.load(f)

tilemap = level_data["tilemap"]
path_points = level_data["path"]
path_pixels = [(x * TILE_SIZE, y * TILE_SIZE) for x, y in path_points]

# Игровые переменные
money = MONEY
base_health = BASE_HEALTH
spawn_timer = 0
enemies = []
waves = level_data["waves"]
current_wave = 0
spawned_enemies = 0
spawn_timer = 0
wave_cooldown = 180  # Пауза между волнами
wave_in_progress = False

towers = []
bullets = []

def spawn_enemy():
    global spawn_timer, spawned_enemies, current_wave, wave_in_progress, enemies

    if current_wave >= len(waves):
        return  # Все волны завершены

    wave = waves[current_wave]
    count = wave["count"]
    health = wave.get("health", 3)
    speed = wave.get("speed", 2)

    if spawned_enemies < count:
        spawn_timer += 1
        spawn_rate = wave.get("spawn_rate", 60)
        if spawn_timer >= spawn_rate:
            enemies.append(Enemy(path_pixels, enemy_img, health=health, speed=speed))
            spawned_enemies += 1
            spawn_timer = 0
            wave_in_progress = True

    # Если волна заспавнена полностью и врагов не осталось — переходим к следующей
    elif not enemies:
        current_wave += 1
        spawned_enemies = 0
        spawn_timer = -wave_cooldown  # Задержка перед следующей волной
        wave_in_progress = False



def update_game():
    global enemies, base_health, money

    for enemy in enemies[:]:  # Делаем копию списка для итерации
        if enemy.update():  # Если враг достиг конца
            base_health -= 1
            enemies.remove(enemy)
        elif enemy.health <= 0:  # Если враг убит
            money += 10
            enemies.remove(enemy)

    for tower in towers:
        tower.update(enemies, bullets)

    for bullet in bullets[:]:
        if not bullet.update():
            bullets.remove(bullet)

    spawn_enemy()
    return enemies


def place_tower(pos):
    global money, towers

    x, y = pos
    grid_x = x // TILE_SIZE
    grid_y = y // TILE_SIZE

    # Проверяем возможность установки
    if (0 <= grid_y < len(tilemap) and (0 <= grid_x < len(tilemap[0]))):
        if tilemap[grid_y][grid_x] == "G" and money >= TOWER_COST:
            for tower in towers:
                if (tower.x // TILE_SIZE) == grid_x and (tower.y // TILE_SIZE) == grid_y:
                    return False


    # Устанавливаем башню
            px = grid_x * TILE_SIZE
            py = grid_y * TILE_SIZE
            towers.append(Tower(px, py, tower_img, bullet_img))
            money -= TOWER_COST
            return True


    return False


def get_money():
    return money

def get_base_health():
    return base_health

def reset_base_health():
    global base_health
    base_health=BASE_HEALTH

def reset_money():
    global money
    money=MONEY

def get_current_wave_number():
    return current_wave + 1

