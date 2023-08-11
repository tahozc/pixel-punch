import pygame
import random

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

class PowerUp:
    def __init__(self):
        self.image = pygame.image.load('powerup.png')
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - 50)
        self.rect.y = random.randint(0, SCREEN_HEIGHT - 50)
        self.type = random.choice(['health', 'speed'])

    def apply(self, fighter):
        if self.type == 'health':
            fighter.health += 20
            if fighter.health > 100:
                fighter.health = 100
        elif self.type == 'speed':
            fighter.vel_x *= 2
            fighter.vel_y *= 2

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
