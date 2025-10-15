import pygame 
import random
from collections import deque
import sys
import time

# Inicialización de Pygame
pygame.init()

# Colores
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (213, 50, 80)
BLUE = (50, 153, 213)
BLACK = (0, 0, 0)

# Dimensiones del tablero
WIDTH = 30
HEIGHT = 25
GRID_SIZE = 15
SCREEN_WIDTH = WIDTH * GRID_SIZE
SCREEN_HEIGHT = HEIGHT * GRID_SIZE
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake con BFS")

# Fuente
font = pygame.font.SysFont("Arial", 20)

# Direcciones
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
ALL_DIRECTIONS = [UP, DOWN, LEFT, RIGHT]

# Clase Snake
class Snake:
    def __init__(self):
        self.body = [(5, 5), (5, 4), (5, 3)]  # Cuerpo inicial
        self.direction = RIGHT
        self.growing = False

    def move(self):
        head_x, head_y = self.body[0]
        dir_x, dir_y = self.direction
        new_head = (head_x + dir_x, head_y + dir_y)
        self.body = [new_head] + self.body
        if not self.growing:
            self.body.pop()
        else:
            self.growing = False

    def grow(self):
        self.growing = True

    def collides_with_boundaries(self):
        head_x, head_y = self.body[0]
        return not (0 <= head_x < WIDTH and 0 <= head_y < HEIGHT)

    def collides_with_self(self):
        return len(self.body) != len(set(self.body))

    def get_head(self):
        return self.body[0]

    def get_direction(self):
        return self.direction

    def set_direction(self, direction):
        self.direction = direction

    def get_positions(self):
        return self.body

# Función para dibujar el tablero
def draw_board(snake, food, score):
    screen.fill(BLACK)
    # Dibujar snake
    for x, y in snake.get_positions():
        pygame.draw.rect(screen, GREEN, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    # Dibujar comida
    fx, fy = food
    pygame.draw.rect(screen, RED, (fx * GRID_SIZE, fy * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    
    # Dibujar score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (5, 5))

    pygame.display.flip()

# Función para generar una nueva manzana
def generate_food(snake):
    while True:
        food = (random.randint(0, WIDTH - 1), random.randint(0, HEIGHT - 1))
        if food not in snake.get_positions():
            return food

# Algoritmo de búsqueda en amplitud (BFS)
def bfs(snake, food):
    start = snake.get_head()
    queue = deque([(start, [])])
    visited = set([start])
    snake_body = set(snake.get_positions()[1:])  # Excluimos la cabeza
    while queue:
        current, path = queue.popleft()
        if current == food:
            return path
        for direction in ALL_DIRECTIONS:
            next_pos = (current[0] + direction[0], current[1] + direction[1])
            if (0 <= next_pos[0] < WIDTH and 0 <= next_pos[1] < HEIGHT and
                next_pos not in visited and next_pos not in snake_body):
                visited.add(next_pos)
                queue.append((next_pos, path + [direction]))
    return []

# Pantalla de Game Over con botón Reset
def game_over_screen(score, elapsed_time):
    screen.fill(BLACK)
    over_text = font.render("GAME OVER", True, RED)
    score_text = font.render(f"Score: {score}", True, WHITE)
    time_text = font.render(f"Tiempo: {elapsed_time}s", True, WHITE)
    
    # Botón reset
    reset_text = font.render("RESET", True, BLACK)
    reset_button = pygame.Rect(SCREEN_WIDTH//5 - 50, SCREEN_HEIGHT//2, 100, 50)
    
    screen.blit(over_text, (SCREEN_WIDTH//2 - over_text.get_width()//2, 100))
    screen.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, 150))
    screen.blit(time_text, (SCREEN_WIDTH//2 - time_text.get_width()//2, 180))
    pygame.draw.rect(screen, WHITE, reset_button)
    screen.blit(reset_text, (reset_button.x + 20, reset_button.y + 10))

    pygame.display.flip()
    
    # Esperar acción del jugador
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if reset_button.collidepoint(event.pos):
                    waiting = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    waiting = False

# Función principal del juego
def game_loop():
    while True:
        snake = Snake()
        food = generate_food(snake)
        clock = pygame.time.Clock()
        score = 0
        start_time = time.time()
        running = True

        while running:
            draw_board(snake, food, score)
            path = bfs(snake, food)
            if path:
                next_direction = path[0]
                snake.set_direction(next_direction)

            snake.move()

            if snake.get_head() == food:
                snake.grow()
                food = generate_food(snake)
                score += 1

            if snake.collides_with_boundaries() or snake.collides_with_self():
                elapsed_time = int(time.time() - start_time)
                game_over_screen(score, elapsed_time)
                running = False

            clock.tick(80)

if __name__ == "__main__":
    game_loop()
