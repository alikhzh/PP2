import pygame
import random
import time
from persistence import load_settings

# constants
WIDTH  = 400
HEIGHT = 600
FPS    = 60

DIFF_MULT = {"easy": 1.6, "normal": 1.0, "hard": 0.55}

CAR_TINTS = {
    "Default": None,
    "Red":     (255, 60,  60),
    "Blue":    (60,  120, 255),
    "Green":   (60,  220, 60),
}


class Player(pygame.sprite.Sprite):
    def __init__(self, image, tint=None):
        super().__init__()
        self.image = image.copy()
        if tint:
            tint_surf = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
            tint_surf.fill((*tint, 120))
            self.image.blit(tint_surf, (0, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom   = HEIGHT - 10
        self.speed  = 5
        self.shield = False

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.rect.move_ip(self.speed, 0)
        if keys[pygame.K_LEFT]:
            self.rect.move_ip(-self.speed, 0)
        if self.rect.left  < 0:     self.rect.left  = 0
        if self.rect.right > WIDTH: self.rect.right = WIDTH


class Enemy(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.rect  = self.image.get_rect()
        self.speed = 10

    def generate_random_rect(self):
        self.rect.left   = random.randint(0, WIDTH - self.rect.w)
        self.rect.bottom = 0

    def move(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > HEIGHT:
            self.generate_random_rect()


class Coin(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.base_image = image
        self.size = random.randint(1, 3)
        self._apply_size()
        self.generate_random_rect()

    def _apply_size(self):
        w = max(8, int(30 * self.size * 0.5))
        self.image = pygame.transform.scale(self.base_image, (w, w))
        self.rect  = self.image.get_rect()

    def generate_random_rect(self):
        self.size = random.randint(1, 3)
        self._apply_size()
        self.rect.left = random.randint(0, WIDTH - self.rect.w)
        self.rect.top  = random.randint(HEIGHT - 80, HEIGHT - 20)


class Obstacle(pygame.sprite.Sprite):
    KINDS = ["oil", "barrier"]

    def __init__(self):
        super().__init__()
        self.kind  = random.choice(self.KINDS)
        self.speed = 4
        w, h = (50, 20) if self.kind == "oil" else (40, 30)
        self.image = pygame.Surface((w, h), pygame.SRCALPHA)
        if self.kind == "oil":
            pygame.draw.ellipse(self.image, (20, 20, 80, 200), (0, 0, w, h))
        else:
            pygame.draw.rect(self.image, (180, 30, 30), (0, 0, w, h))
            pygame.draw.rect(self.image, (255, 255, 255), (0, 0, w, h), 2)
        self.rect = self.image.get_rect()
        self._spawn()

    def _spawn(self):
        self.rect.left   = random.randint(0, WIDTH - self.rect.w)
        self.rect.bottom = 0

    def move(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > HEIGHT:
            self._spawn()


class NitroStrip(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((WIDTH, 14), pygame.SRCALPHA)
        self.image.fill((255, 220, 0, 160))
        self.rect        = self.image.get_rect()
        self.rect.bottom = 0
        self.speed       = 5

    def move(self):
        self.rect.move_ip(0, self.speed)


POWERUP_COLORS = {"nitro": (255, 160, 0), "shield": (80, 80, 255), "repair": (0, 200, 80)}


class PowerUp(pygame.sprite.Sprite):
    TIMEOUT = 7000

    def __init__(self, kind):
        super().__init__()
        self.kind  = kind
        self.speed = 4
        self.image = pygame.Surface((28, 28), pygame.SRCALPHA)
        pygame.draw.circle(self.image, POWERUP_COLORS[kind], (14, 14), 14)
        label = pygame.font.SysFont("Verdana", 11).render(kind[0].upper(), True, (0, 0, 0))
        self.image.blit(label, label.get_rect(center=(14, 14)))
        self.rect        = self.image.get_rect()
        self.rect.left   = random.randint(0, WIDTH - self.rect.w)
        self.rect.bottom = 0
        self.spawned_at  = pygame.time.get_ticks()

    def move(self):
        self.rect.move_ip(0, self.speed)

    def expired(self):
        return pygame.time.get_ticks() - self.spawned_at > self.TIMEOUT or self.rect.top > HEIGHT


def draw_hud(screen, fontt, collected, distance, active_pu, pu_end):
    hud = pygame.Surface((320, 32), pygame.SRCALPHA)
    hud.fill((0, 0, 0, 140))
    screen.blit(hud, (0, 0))
    screen.blit(fontt.render(f"Score:{collected}  Dist:{int(distance)}m", True, (255, 255, 255)), (5, 5))
    if active_pu:
        remaining = max(0, (pu_end - pygame.time.get_ticks()) // 1000)
        label = f"{active_pu.upper()} {remaining}s" if remaining else active_pu.upper()
        screen.blit(fontt.render(label, True, POWERUP_COLORS[active_pu]), (5, 32))


def play_game(screen, username):
    settings  = load_settings()
    diff_mult = DIFF_MULT.get(settings.get("difficulty", "normal"), 1.0)
    tint      = CAR_TINTS.get(settings.get("car_color", "Default"))

    # ── фон из assets ─────────────────────────────────────────────────────
    try:
        image_background = pygame.image.load('assets/AnimatedStreet.png').convert()
        image_background = pygame.transform.scale(image_background, (WIDTH, HEIGHT))
    except Exception as e:
        print(f"[WARNING] AnimatedStreet.png: {e}")
        # запасной процедурный фон
        image_background = pygame.Surface((WIDTH, HEIGHT))
        image_background.fill((70, 70, 70))
        pygame.draw.rect(image_background, (200, 200, 200), (38, 0, 4, HEIGHT))
        pygame.draw.rect(image_background, (200, 200, 200), (WIDTH - 42, 0, 4, HEIGHT))
        for y in range(0, HEIGHT, 60):
            pygame.draw.rect(image_background, (255, 220, 0), (WIDTH // 2 - 4, y, 8, 36))

    # ── спрайты из assets ─────────────────────────────────────────────────
    try:
        image_player = pygame.image.load('assets/Player.png').convert_alpha()
        image_player = pygame.transform.scale(image_player, (40, 70))
    except Exception as e:
        print(f"[WARNING] Player.png: {e}")
        image_player = pygame.Surface((40, 70), pygame.SRCALPHA)
        image_player.fill((0, 180, 255))

    try:
        image_enemy = pygame.image.load('assets/Enemy.png').convert_alpha()
        image_enemy = pygame.transform.scale(image_enemy, (40, 70))
    except Exception as e:
        print(f"[WARNING] Enemy.png: {e}")
        image_enemy = pygame.Surface((40, 70), pygame.SRCALPHA)
        image_enemy.fill((220, 50, 50))

    try:
        coin_image = pygame.image.load('assets/dollar.png').convert_alpha()
    except Exception as e:
        print(f"[WARNING] dollar.png: {e}")
        coin_image = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(coin_image, (255, 215, 0), (15, 15), 15)

    # ── музыка ────────────────────────────────────────────────────────────
    if settings.get("sound", True):
        try:
            pygame.mixer.music.stop()
            pygame.mixer.music.load('assets/background.wav')
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)
        except Exception as e:
            print(f"[WARNING] background.wav: {e}")

    sound_crash = None
    if settings.get("sound", True):
        try:
            sound_crash = pygame.mixer.Sound('assets/crash.wav')
        except Exception as e:
            print(f"[WARNING] crash.wav: {e}")

    fontt = pygame.font.SysFont("Verdana", 20)

    # ── спрайты ───────────────────────────────────────────────────────────
    player = Player(image_player, tint)
    enemy  = Enemy(image_enemy)
    coin   = Coin(coin_image)
    enemy.generate_random_rect()

    all_sprites      = pygame.sprite.Group(player, enemy, coin)
    enemy_sprites    = pygame.sprite.Group(enemy)
    coin_sprites     = pygame.sprite.Group(coin)
    obstacle_sprites = pygame.sprite.Group()
    powerup_sprites  = pygame.sprite.Group()
    nitro_sprites    = pygame.sprite.Group()

    clock        = pygame.time.Clock()
    collected    = 0
    distance     = 0.0
    last_speedup = 0
    N = 5

    last_obstacle     = pygame.time.get_ticks()
    last_powerup      = pygame.time.get_ticks()
    last_nitro        = pygame.time.get_ticks()
    OBSTACLE_INTERVAL = int(3000 * diff_mult)
    POWERUP_INTERVAL  = int(8000 * diff_mult)
    NITRO_INTERVAL    = int(12000 * diff_mult)

    active_pu    = None
    pu_end       = 0
    base_speed   = player.speed
    oil_slow     = False
    oil_slow_end = 0
    bg_y         = 0

    running = True
    while running:
        now = pygame.time.get_ticks()

        # ── события ───────────────────────────────────────────────────────
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.USEREVENT + 1:
                if active_pu != "nitro":
                    player.speed = base_speed

        # ── спавн препятствий ─────────────────────────────────────────────
        if now - last_obstacle > OBSTACLE_INTERVAL:
            obs = Obstacle()
            attempts = 0
            while abs(obs.rect.centerx - player.rect.centerx) < 40 and attempts < 10:
                obs._spawn()
                attempts += 1
            obstacle_sprites.add(obs)
            all_sprites.add(obs)
            last_obstacle = now
            OBSTACLE_INTERVAL = max(800, OBSTACLE_INTERVAL - 40)

        # ── спавн пауэр-апа ───────────────────────────────────────────────
        if now - last_powerup > POWERUP_INTERVAL and len(powerup_sprites) == 0:
            kind = random.choice(["nitro", "shield", "repair"])
            pu = PowerUp(kind)
            powerup_sprites.add(pu)
            all_sprites.add(pu)
            last_powerup = now

        # ── спавн nitro-полосы ────────────────────────────────────────────
        if now - last_nitro > NITRO_INTERVAL:
            ns = NitroStrip()
            nitro_sprites.add(ns)
            all_sprites.add(ns)
            last_nitro = now

        # ── истечение пауэр-апов ──────────────────────────────────────────
        for pu in list(powerup_sprites):
            if pu.expired():
                pu.kill()

        if active_pu == "nitro" and now > pu_end:
            player.speed = base_speed
            active_pu = None
        if oil_slow and now > oil_slow_end:
            player.speed = base_speed if active_pu != "nitro" else base_speed + 4
            oil_slow = False

        # ── движение ─────────────────────────────────────────────────────
        player.move()
        enemy.move()
        for obs in obstacle_sprites:
            obs.move()
        for pu in powerup_sprites:
            pu.move()
        for ns in list(nitro_sprites):
            ns.move()
            if ns.rect.top > HEIGHT:
                ns.kill()

        # ── коллизия с монетой ────────────────────────────────────────────
        if pygame.sprite.spritecollideany(player, coin_sprites):
            collected += coin.size
            if collected // N > last_speedup:
                enemy.speed += 3
                last_speedup = collected // N
            coin.generate_random_rect()

        # ── коллизия с препятствием ───────────────────────────────────────
        hit_obs = pygame.sprite.spritecollideany(player, obstacle_sprites)
        if hit_obs:
            if hit_obs.kind == "barrier":
                if player.shield:
                    player.shield = False
                    active_pu = None
                    hit_obs.kill()
                else:
                    running = False
            elif hit_obs.kind == "oil":
                if not oil_slow:
                    oil_slow = True
                    oil_slow_end = now + 2000
                    player.speed = max(2, player.speed - 2)
                hit_obs.kill()

        # ── коллизия с врагом ─────────────────────────────────────────────
        if pygame.sprite.spritecollideany(player, enemy_sprites):
            if player.shield:
                player.shield = False
                active_pu = None
                enemy.generate_random_rect()
            else:
                running = False

        # ── подбор пауэр-апа ─────────────────────────────────────────────
        hit_pu = pygame.sprite.spritecollideany(player, powerup_sprites)
        if hit_pu:
            if hit_pu.kind == "nitro":
                active_pu    = "nitro"
                pu_end       = now + 4000
                player.speed = base_speed + 4
            elif hit_pu.kind == "shield":
                active_pu     = "shield"
                player.shield = True
            elif hit_pu.kind == "repair":
                for obs in list(obstacle_sprites)[:1]:
                    obs.kill()
            hit_pu.kill()

        # ── nitro-полоса ──────────────────────────────────────────────────
        if pygame.sprite.spritecollideany(player, nitro_sprites):
            if active_pu != "nitro":
                player.speed = base_speed + 3
                pygame.time.set_timer(pygame.USEREVENT + 1, 1500, 1)

        distance += player.speed * 0.05

        # ── отрисовка ─────────────────────────────────────────────────────
        bg_y = (bg_y + 5) % HEIGHT
        screen.blit(image_background, (0, bg_y - HEIGHT))
        screen.blit(image_background, (0, bg_y))

        for ns in nitro_sprites:
            screen.blit(ns.image, ns.rect)
        for obs in obstacle_sprites:
            screen.blit(obs.image, obs.rect)
        for pu in powerup_sprites:
            screen.blit(pu.image, pu.rect)
        screen.blit(coin.image, coin.rect)
        screen.blit(enemy.image, enemy.rect)
        screen.blit(player.image, player.rect)

        draw_hud(screen, fontt, collected, distance, active_pu, pu_end)
        pygame.display.flip()
        clock.tick(FPS)

    # ── конец игры ────────────────────────────────────────────────────────
    if sound_crash:
        sound_crash.play()
    pygame.mixer.music.stop()
    time.sleep(0.5)

    return collected, distance