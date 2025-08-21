import pygame
import sys
import random
import os

# Настройки
WINDOW_SIZE = 600
CELL_SIZE = 20
GRID_COLOR = (50, 50, 50)
BASE_FPS = 10
SPEED_INCREMENT = 0.5

# Путь к папке assets
ASSETS_PATH = "assets"

# Инициализация Pygame
pygame.init()
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# Загружаем текстуры
snake_img = pygame.image.load(os.path.join(ASSETS_PATH, "snake.png")).convert_alpha()
snake_img = pygame.transform.scale(snake_img, (CELL_SIZE, CELL_SIZE))
food_img = pygame.image.load(os.path.join(ASSETS_PATH, "food.png")).convert_alpha()
food_img = pygame.transform.scale(food_img, (CELL_SIZE, CELL_SIZE))

# Начальные параметры змейки
def init_snake():
    return [(5, 5), (5, 6), (5, 7)]

snake = init_snake()
direction = (0, -1)

# Еда
def spawn_food():
    while True:
        pos = (random.randint(0, (WINDOW_SIZE//CELL_SIZE)-1),
               random.randint(0, (WINDOW_SIZE//CELL_SIZE)-1))
        if pos not in snake:
            return pos

food = spawn_food()
score = 0
fps = BASE_FPS

# Отрисовка
def draw_grid():
    for x in range(0, WINDOW_SIZE, CELL_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, WINDOW_SIZE))
    for y in range(0, WINDOW_SIZE, CELL_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (WINDOW_SIZE, y))

def draw_snake():
    for segment in snake:
        screen.blit(snake_img, (segment[0]*CELL_SIZE, segment[1]*CELL_SIZE))

def draw_food():
    screen.blit(food_img, (food[0]*CELL_SIZE, food[1]*CELL_SIZE))

def draw_score():
    text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(text, (10, 10))

# Основной цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != (0, 1):
                direction = (0, -1)
            elif event.key == pygame.K_DOWN and direction != (0, -1):
                direction = (0, 1)
            elif event.key == pygame.K_LEFT and direction != (1, 0):
                direction = (-1, 0)
            elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                direction = (1, 0)

    # Двигаем змейку
    head_x, head_y = snake[-1]
    new_head = (head_x + direction[0], head_y + direction[1])

    # Проверка столкновений
    if (new_head in snake) or not (0 <= new_head[0] < WINDOW_SIZE//CELL_SIZE) or not (0 <= new_head[1] < WINDOW_SIZE//CELL_SIZE):
        snake = init_snake()
        direction = (0, -1)
        food = spawn_food()
        score = 0
        fps = BASE_FPS
    else:
        snake.append(new_head)
        if new_head == food:
            score += 1
            fps = BASE_FPS + score * SPEED_INCREMENT
            food = spawn_food()
        else:
            snake.pop(0)

    # Отрисовка
    screen.fill((0, 0, 0))
    draw_grid()
    draw_snake()
    draw_food()
    draw_score()
    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
sys.exit()
