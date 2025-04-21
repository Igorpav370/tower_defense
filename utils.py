from collections import deque

def find_path_with_edge(tilemap):
    height = len(tilemap)
    if height == 0:
        return []
    width = len(tilemap[0])

    # Проверка, находится ли точка на краю
    def is_edge(x, y):
        return x == 0 or x == width - 1 or y == 0 or y == height - 1

    # Находим все точки на краях
    edge_points = []
    for y in range(height):
        for x in range(width):
            if tilemap[y][x] == "#" and is_edge(x, y):
                edge_points.append((x, y))

    if not edge_points:
        return []

    # Выбираем стартовую точку (первую на верхнем краю)
    start_x, start_y = edge_points[0]
    for x, y in edge_points:
        if y == 0:
            start_x, start_y = x, y
            break

    # Построение пути вдоль края
    path = []
    visited = set()
    x, y = start_x, start_y

    # Двигаемся вдоль края (приоритет: право → вниз → влево → вверх)
    while True:
        path.append([x, y])
        visited.add((x, y))

        moved = False
        for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height:
                if tilemap[ny][nx] == "#" and (nx, ny) not in visited and is_edge(nx, ny):
                    x, y = nx, ny
                    moved = True
                    break

        if not moved:
            break

    # Если остались непосещённые точки, продолжаем BFS внутрь
    remaining_points = set()
    for y in range(height):
        for x in range(width):
            if tilemap[y][x] == "#" and (x, y) not in visited:
                remaining_points.add((x, y))

    if remaining_points:
        # BFS для поиска кратчайшего пути от последней точки до любого края
        queue = deque()
        queue.append((x, y, path.copy()))
        found_path = None

        while queue:
            current_x, current_y, current_path = queue.popleft()

            if is_edge(current_x, current_y) and (current_x, current_y) != (start_x, start_y):
                found_path = current_path
                break

            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nx, ny = current_x + dx, current_y + dy
                if 0 <= nx < width and 0 <= ny < height:
                    if tilemap[ny][nx] == "#" and (nx, ny) not in visited:
                        visited.add((nx, ny))
                        queue.append((nx, ny, current_path + [[nx, ny]]))

        if found_path:
            path = found_path

    return path


def generate_path(tilemap):
    height = len(tilemap)
    width = len(tilemap[0]) if height > 0 else 0

    # Находим все клетки с "#"
    all_points = set()
    for y in range(height):
        for x in range(width):
            if tilemap[y][x] == "#":
                all_points.add((x, y))

    if not all_points:
        return []

    # Стартовая точка — первая "#" в первой строке
    start_x, start_y = -1, -1
    for y in range(height):
        for x in range(width):
            if tilemap[y][x] == "#":
                start_x, start_y = x, y
                break
        if start_x != -1:
            break

    path = []
    visited = set()
    x, y = start_x, start_y

    while True:
        path.append([x, y])
        visited.add((x, y))

        # Приоритет направлений: вправо → вниз → влево → вверх
        moved = False
        for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height:
                if tilemap[ny][nx] == "#" and (nx, ny) not in visited:
                    x, y = nx, ny
                    moved = True
                    break

        if not moved:
            break

    return path

