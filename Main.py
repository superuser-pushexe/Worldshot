import pygame
import math
import random

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
PLAYER_SIZE = 50
BULLET_SIZE = 10
ENEMY_SIZE = 40
PLAYER_SPEED = 5
BULLET_SPEED = 10
ENEMY_SPEED = 3
NUM_ENEMIES = 5
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Setup the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2D FPS Simulation")

# Load images
player_image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
player_image.fill(GREEN)
bullet_image = pygame.Surface((BULLET_SIZE, BULLET_SIZE))
bullet_image.fill(RED)
enemy_image = pygame.Surface((ENEMY_SIZE, ENEMY_SIZE))
enemy_image.fill(BLACK)

# Game objects
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.angle = 0

    def rotate(self, angle):
        self.angle = angle
        rotated_image = pygame.transform.rotate(player_image, self.angle)
        self.image = rotated_image
        self.rect = self.image.get_rect(center=self.rect.center)

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - PLAYER_SIZE))
        self.rect.y = max(0, min(self.rect.y, SCREEN_HEIGHT - PLAYER_SIZE))

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        super().__init__()
        self.image = bullet_image
        self.rect = self.image.get_rect(center=(x, y))
        self.angle = angle
        self.dx = BULLET_SPEED * math.cos(math.radians(angle))
        self.dy = -BULLET_SPEED * math.sin(math.radians(angle))

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy
        if (self.rect.x < 0 or self.rect.x > SCREEN_WIDTH or
            self.rect.y < 0 or self.rect.y > SCREEN_HEIGHT):
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = enemy_image
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.rect.x += ENEMY_SPEED
        if self.rect.x > SCREEN_WIDTH or self.rect.x < 0:
            self.kill()

# Create groups
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()

# Create player
player = Player()
all_sprites.add(player)

# Create enemies
for _ in range(NUM_ENEMIES):
    enemy = Enemy(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))
    all_sprites.add(enemy)
    enemies.add(enemy)

# Main game loop
clock = pygame.time.Clock()
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Key presses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move(-PLAYER_SPEED, 0)
    if keys[pygame.K_RIGHT]:
        player.move(PLAYER_SPEED, 0)
    if keys[pygame.K_UP]:
        player.move(0, -PLAYER_SPEED)
    if keys[pygame.K_DOWN]:
        player.move(0, PLAYER_SPEED)

    # Mouse controls
    mouse_x, mouse_y = pygame.mouse.get_pos()
    player_center_x = player.rect.centerx
    player_center_y = player.rect.centery

    # Calculate angle from player to mouse
    dx = mouse_x - player_center_x
    dy = mouse_y - player_center_y
    player_angle = math.degrees(math.atan2(-dy, dx))

    player.rotate(player_angle)

    if pygame.mouse.get_pressed()[0]:
        bullet = Bullet(player_center_x, player_center_y, player_angle)
        all_sprites.add(bullet)
        bullets.add(bullet)
        pygame.time.wait(30)  # Delay to prevent rapid firing

    # Update game objects
    all_sprites.update()

    # Check for collisions
    collisions = pygame.sprite.groupcollide(bullets, enemies, True, True)

    # Draw everything
    screen.fill(WHITE)
    all_sprites.draw(screen)
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

pygame.quit()
