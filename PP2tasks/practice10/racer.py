import pygame
import random
import sys

pygame.init()

# ── Constants ─────────────────────────────────────────────
SCREEN_W, SCREEN_H = 400, 600
FPS = 60

ROAD_LEFT  = 60
ROAD_RIGHT = 340
LANE_W     = (ROAD_RIGHT - ROAD_LEFT) // 3

WHITE  = (255, 255, 255)
BLACK  = (0, 0, 0)
GRAY   = (90, 90, 90)
DKGRAY = (50, 50, 50)
YELLOW = (255, 215, 0)
GOLD   = (200, 160, 0)
RED    = (210, 30, 30)
BLUE   = (30, 90, 210)
LT_BLU = (160, 210, 255)
GRASS  = (45, 120, 45)

screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("Racer")
clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 22, bold=True)
big = pygame.font.SysFont("Arial", 48, bold=True)
small = pygame.font.SysFont("Arial", 14, bold=True)


def random_lane_x(obj_width: int) -> int:
    lane = random.randint(0, 2)
    return ROAD_LEFT + lane * LANE_W + (LANE_W - obj_width) // 2


# ── Road ─────────────────────────────────────────────
class Road:
    LINE_H = 55
    LINE_GAP = 35
    SEGMENT = LINE_H + LINE_GAP

    def __init__(self):
        self.offset = 0
        self.speed = 5

    def update(self):
        self.offset = (self.offset + self.speed) % self.SEGMENT

    def draw(self, surface):
        surface.fill(GRASS)

        pygame.draw.rect(surface, GRAY, (ROAD_LEFT, 0, ROAD_RIGHT - ROAD_LEFT, SCREEN_H))

        pygame.draw.rect(surface, WHITE, (ROAD_LEFT - 4, 0, 4, SCREEN_H))
        pygame.draw.rect(surface, WHITE, (ROAD_RIGHT, 0, 4, SCREEN_H))

        for lane in range(1, 3):
            x = ROAD_LEFT + LANE_W * lane - 2
            y = self.offset - self.SEGMENT
            while y < SCREEN_H:
                pygame.draw.rect(surface, WHITE, (x, y, 4, self.LINE_H))
                y += self.SEGMENT


# ── Player ─────────────────────────────────────────────
class PlayerCar:
    W, H = 38, 68

    def __init__(self):
        self.x = SCREEN_W // 2 - self.W // 2
        self.y = SCREEN_H - 110
        self.spd = 5

    def draw(self, surface):
        x, y, w, h = self.x, self.y, self.W, self.H

        pygame.draw.rect(surface, BLUE, (x, y, w, h), border_radius=6)
        pygame.draw.rect(surface, LT_BLU, (x+5, y+8, w-10, 18))
        pygame.draw.rect(surface, LT_BLU, (x+5, y+h-22, w-10, 12))

        for wx, wy in [(x-6, y+6), (x+w-2, y+6), (x-6, y+h-22), (x+w-2, y+h-22)]:
            pygame.draw.rect(surface, BLACK, (wx, wy, 8, 14))

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x > ROAD_LEFT:
            self.x -= self.spd
        if keys[pygame.K_RIGHT] and self.x + self.W < ROAD_RIGHT:
            self.x += self.spd
        if keys[pygame.K_UP] and self.y > 0:
            self.y -= self.spd
        if keys[pygame.K_DOWN] and self.y + self.H < SCREEN_H:
            self.y += self.spd

    def rect(self):
        return pygame.Rect(self.x, self.y, self.W, self.H)


# ── Enemy ─────────────────────────────────────────────
class EnemyCar:
    W, H = 38, 68

    def __init__(self, speed):
        self.x = random_lane_x(self.W)
        self.y = -self.H
        self.spd = speed
        self.col = random.choice([(200, 40, 40), (180, 90, 0), (140, 0, 140)])

    def update(self):
        self.y += self.spd

    def draw(self, surface):
        pygame.draw.rect(surface, self.col, (self.x, self.y, self.W, self.H), border_radius=6)

    def off_screen(self):
        return self.y > SCREEN_H

    def rect(self):
        return pygame.Rect(self.x, self.y, self.W, self.H)


# ── Coin ─────────────────────────────────────────────
class Coin:
    R = 11

    def __init__(self, speed):
        self.x = random.randint(ROAD_LEFT + self.R, ROAD_RIGHT - self.R)
        self.y = -self.R
        self.spd = speed

    def update(self):
        self.y += self.spd

    def draw(self, surface):
        pygame.draw.circle(surface, YELLOW, (self.x, self.y), self.R)
        pygame.draw.circle(surface, GOLD, (self.x, self.y), self.R, 2)

    def rect(self):
        return pygame.Rect(self.x-self.R, self.y-self.R, self.R*2, self.R*2)

    def off_screen(self):
        return self.y > SCREEN_H


# ── HUD ─────────────────────────────────────────────
def draw_hud(score, coins):
    s = font.render(f"Score: {score}", True, WHITE)
    c = font.render(f"Coins: {coins}", True, YELLOW)
    screen.blit(s, (10, 10))
    screen.blit(c, (SCREEN_W - 130, 10))


def draw_game_over(score, coins):
    overlay = pygame.Surface((SCREEN_W, SCREEN_H))
    overlay.set_alpha(180)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))

    text = big.render("GAME OVER", True, RED)
    screen.blit(text, (80, 200))


# ── MAIN ─────────────────────────────────────────────
def main():
    road = Road()
    player = PlayerCar()

    enemies = []
    coins = []

    score = 0
    coin_count = 0
    game_over = False

    enemy_timer = 0
    coin_timer = 0

    while True:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if not game_over:
            keys = pygame.key.get_pressed()
            player.move(keys)

            road.update()

            enemy_timer += 1
            coin_timer += 1

            if enemy_timer > 80:
                enemies.append(EnemyCar(4))
                enemy_timer = 0

            if coin_timer > 120:
                coins.append(Coin(3))
                coin_timer = 0

            for e in enemies[:]:
                e.update()
                if e.off_screen():
                    enemies.remove(e)
                    score += 1
                elif e.rect().colliderect(player.rect()):
                    game_over = True

            for c in coins[:]:
                c.update()
                if c.off_screen():
                    coins.remove(c)
                elif c.rect().colliderect(player.rect()):
                    coins.remove(c)
                    coin_count += 1

        road.draw(screen)

        for e in enemies:
            e.draw(screen)
        for c in coins:
            c.draw(screen)

        player.draw(screen)

        draw_hud(score, coin_count)

        if game_over:
            draw_game_over(score, coin_count)

        pygame.display.update()


if __name__ == "__main__":
    main()