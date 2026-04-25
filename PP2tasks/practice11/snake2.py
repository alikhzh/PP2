import pygame, sys, random
from pygame.locals import *

pygame.init()

# ── Grid settings ─────────────────────────────────────
CELL_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 20
WIDTH = CELL_SIZE * GRID_WIDTH
HEIGHT = CELL_SIZE * GRID_HEIGHT

# ── Colors ────────────────────────────────────────────
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# разные цвета еды
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
PURPLE = (180, 0, 255)

DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

font = pygame.font.SysFont("Verdana", 18)

# ── Snake ─────────────────────────────────────────────
class Snake:
    def __init__(self):
        self.body = [(10, 10), (9, 10), (8, 10)]
        self.direction = (1, 0)
        self.grow = False
        
    def update(self):
        head_x, head_y = self.body[0]
        dx, dy = self.direction

        # новая позиция головы
        new_head = (head_x + dx, head_y + dy)
        self.body.insert(0, new_head)
        
        # если не растём — удаляем хвост
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False
            
    def draw(self, surface):
        for segment in self.body:
            rect = pygame.Rect(segment[0]*CELL_SIZE, segment[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(surface, GREEN, rect)


# ── Food (UPDATED) ─────────────────────────────────────
class Food:
    def __init__(self, snake_body):
        self.randomize(snake_body)

    def randomize(self, snake_body):
        # случайная позиция (не на змее)
        while True:
            pos = (random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1))
            if pos not in snake_body:
                self.position = pos
                break

        # 🎯 случайный вес еды
        self.value = random.choice([10, 20, 30])

        # цвет зависит от веса
        if self.value == 10:
            self.color = RED
        elif self.value == 20:
            self.color = ORANGE
        else:
            self.color = PURPLE

        # ⏳ таймер жизни (в кадрах)
        self.timer = random.randint(80, 150)

    def update(self, snake_body):
        # уменьшаем таймер
        self.timer -= 1

        # если время вышло — создаём новую еду
        if self.timer <= 0:
            self.randomize(snake_body)

    def draw(self, surface):
        rect = pygame.Rect(
            self.position[0]*CELL_SIZE,
            self.position[1]*CELL_SIZE,
            CELL_SIZE,
            CELL_SIZE
        )
        pygame.draw.rect(surface, self.color, rect)


# ── MAIN ─────────────────────────────────────────────
def main():
    snake = Snake()
    food = Food(snake.body)
    
    score = 0
    level = 1
    base_fps = 8
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == KEYDOWN:
                if event.key == K_UP and snake.direction != (0, 1):
                    snake.direction = (0, -1)
                elif event.key == K_DOWN and snake.direction != (0, -1):
                    snake.direction = (0, 1)
                elif event.key == K_LEFT and snake.direction != (1, 0):
                    snake.direction = (-1, 0)
                elif event.key == K_RIGHT and snake.direction != (-1, 0):
                    snake.direction = (1, 0)
        
        snake.update()

        # ── Проверка столкновений ─────────────────────
        head_x, head_y = snake.body[0]

        # стены
        if head_x < 0 or head_x >= GRID_WIDTH or head_y < 0 or head_y >= GRID_HEIGHT:
            print(f"Game Over! Score: {score}")
            pygame.quit()
            sys.exit()

        # сам в себя
        if snake.body[0] in snake.body[1:]:
            print(f"Game Over! Score: {score}")
            pygame.quit()
            sys.exit()

        # ── Обновляем еду (таймер!) ───────────────────
        food.update(snake.body)

        # ── Съели еду ─────────────────────────────────
        if snake.body[0] == food.position:
            snake.grow = True

            # ➕ добавляем очки по весу
            score += food.value

            # новая еда
            food.randomize(snake.body)

            # уровень
            if score % 50 == 0:
                level += 1
                base_fps += 1

        # ── DRAW ─────────────────────────────────────
        DISPLAYSURF.fill(BLACK)

        snake.draw(DISPLAYSURF)
        food.draw(DISPLAYSURF)

        score_txt = font.render(f"Score: {score}", True, WHITE)
        level_txt = font.render(f"Level: {level}", True, WHITE)

        DISPLAYSURF.blit(score_txt, (10, 10))
        DISPLAYSURF.blit(level_txt, (10, 30))

        pygame.display.update()
        clock.tick(base_fps)


if __name__ == "__main__":
    main()