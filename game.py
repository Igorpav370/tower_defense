import pygame
import json
import utils
from entities.enemy import BasicEnemy, TankEnemy, FastEnemy
from entities.tower import BasicTower, AdvancedTower
from config import *
from pathlib import Path

# === Загрузка ресурсов ===
assets_dir = Path("assets")
tileset = {
    " ": pygame.image.load(assets_dir / "tiles" / "grass.png"),
    "#": pygame.image.load(assets_dir / "tiles" / "path.png")
}
# Загрузка изображений башен
tower_images = {
    "basic": pygame.image.load(assets_dir / "towers" / "basic_tower.png"),
    "advanced": pygame.image.load(assets_dir / "towers" / "advanced_tower.png"),
}
# Загрузка изображений пуль
bullet_images = {
    "basic": pygame.image.load(assets_dir / "towers" / "bullet.png").convert_alpha(),
    "advanced": pygame.image.load(assets_dir / "towers" / "advanced_bullet.png").convert_alpha(),            
}
# Загрузка изображений врагов
enemy_images = {
    "basic": pygame.image.load(assets_dir / "enemies" / "basic_enemy2.png").convert_alpha(),
    "tank": pygame.image.load(assets_dir / "enemies" / "tank_enemy.png").convert_alpha(),
    "fast": pygame.image.load(assets_dir / "enemies" / "fast_enemy.png").convert_alpha(),
}
# Сопоставление типа врага и класса
enemy_classes = {
    "basic": BasicEnemy,
    "tank": TankEnemy,
    "fast": FastEnemy,
}
# Сопоставление типа башни и класса
tower_classes = {
    "basic": BasicTower,
    "advanced": AdvancedTower,
}

# === Загрузка карты ===
with open("levels/level1.json", "r") as f:
    level_data = json.load(f)

tilemap = level_data["tilemap"]
path_points = utils.generate_path(tilemap)
path_pixels = [(x * TILE_SIZE, y * TILE_SIZE) for x, y in path_points]

# === Игровые переменные ===
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
win_game = False
enemies_left = utils.get_total_enemies_in_wave(0, waves)

towers = []
bullets = []

def spawn_enemy():
    global spawn_timer, spawned_enemies, current_wave, wave_in_progress, enemies, money, win_game, enemies_left
    
    if current_wave >= len(waves):
        win_game = True
        return

    wave = waves[current_wave]
    enemy_groups = wave.get("enemies", [])
    spawn_rate = wave.get("spawn_rate", 60)

    # Следим за текущей группой врагов в волне
    if "group_index" not in wave:
        wave["group_index"] = 0
        wave["group_spawned"] = 0

    if wave["group_index"] >= len(enemy_groups):
        if not enemies:
            # Переход к следующей волне
            current_wave += 1
            spawn_timer = -wave_cooldown
            wave_in_progress = False
            money += 50 + current_wave * 5
            enemies_left = utils.get_total_enemies_in_wave(current_wave, waves)
        return

    group = enemy_groups[wave["group_index"]]
    group_count = group["count"]
    group_type = group["type"]

    enemy_class = enemy_classes.get(group_type, BasicEnemy)
    enemy_img = enemy_images.get(group_type, enemy_images["basic"])

    spawn_timer += 1
    if spawn_timer >= spawn_rate:
        spawn_timer = 0
        enemies.append(enemy_class(path_pixels, enemy_img))
        wave["group_spawned"] += 1
        wave_in_progress = True

        # Если вся группа заспавнена — переходим к следующей
        if wave["group_spawned"] >= group_count:
            wave["group_index"] += 1
            wave["group_spawned"] = 0


def update_game():
    global enemies, base_health, money, enemies_left

    for bullet in bullets[:]:
        if not bullet.update():
            bullets.remove(bullet)

    for enemy in enemies[:]:  # Делаем копию списка для итерации
        if enemy.update():  # Если враг достиг конца
            base_health -= 1
            enemies.remove(enemy)
            enemies_left -= 1
        elif enemy.health <= 0:  # Если враг убит
            money += enemy.reward
            enemies.remove(enemy)
            enemies_left -= 1

    for tower in towers:
        tower.update(enemies, bullets)

    spawn_enemy()
    return enemies


def place_tower(pos, tower_type="advanced"):
    global money, towers

    x, y = pos
    grid_x = x // TILE_SIZE
    grid_y = y // TILE_SIZE

    if (0 <= grid_y < len(tilemap) and (0 <= grid_x < len(tilemap[0]))):
        if tilemap[grid_y][grid_x] == " ":
            for tower in towers:
                if (tower.x // TILE_SIZE) == grid_x and (tower.y // TILE_SIZE) == grid_y:
                    return False

            tower_class = tower_classes.get(tower_type, AdvancedTower)
            tower_image = tower_images.get(tower_type, tower_images["advanced"])
            bullet_image = bullet_images.get(tower_type, bullet_images["basic"])

            # ← Создаём временный объект, чтобы узнать цену
            temp_tower = tower_class(-1000, -1000, tower_image, bullet_img=bullet_image)
            if money >= temp_tower.cost:
                px = grid_x * TILE_SIZE
                py = grid_y * TILE_SIZE
                towers.append(tower_class(px, py, tower_image, bullet_img=bullet_image))
                money -= temp_tower.cost
                return True

    return False


def get_money():
    return money

def get_base_health():
    return base_health

def get_current_wave_number():
    return current_wave + 1

def get_win_status():
    return win_game

def get_enemies_left():
    return enemies_left

def reset_game():
    global current_wave, spawn_timer, wave_in_progress, enemies, money, enemies_left
    global money
    money=MONEY

    global base_health
    base_health=BASE_HEALTH

    current_wave = 0
    spawn_timer = 0
    wave_in_progress = False
    enemies.clear()
    money = 100
    enemies_left = utils.get_total_enemies_in_wave(0, waves)

    # Сброс прогресса внутри волн
    for wave in waves:
        wave["group_index"] = 0
        wave["group_spawned"] = 0