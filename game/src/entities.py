# entities.py
import pygame
import random
from settings import WIDTH, HEIGHT, PLAYER_SPEED
from assets_loader import load_player_images, load_tire_image, load_waterdrop_image

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.images = load_player_images()
        self.image = self.images["default"]
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH // 2
        self.rect.y = HEIGHT - 60
        self.health = 100

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.image = self.images["left"]
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.image = self.images["right"]
            self.rect.x += PLAYER_SPEED

        # Limitar el movimiento
        self.rect.x = max(0, min(self.rect.x, WIDTH - self.rect.width))

class Tire(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_tire_image()
        self.rect = self.image.get_rect()
        self.reset_position()

    def reset_position(self):
        self.rect.x = random.randint(0, WIDTH - 30)
        self.rect.y = random.randint(-100, -30)

    def update(self):
        self.rect.y += 5
        if self.rect.y > HEIGHT:
            self.reset_position()

class WaterDrop(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_waterdrop_image()
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - 30)
        self.rect.y = random.randint(-100, -30)

    def update(self):
        self.rect.y += 10
        if self.rect.y > HEIGHT:
            self.kill()
