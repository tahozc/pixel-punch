import pygame

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

class Arena:
    def __init__(self):
        self.platforms = [pygame.Rect(SCREEN_WIDTH * 0.25, SCREEN_HEIGHT * 0.6, 200, 10),
                          pygame.Rect(SCREEN_WIDTH * 0.75 - 200, SCREEN_HEIGHT * 0.6, 200, 10)]

    def check_collisions(self, fighter):
        """
        Function to check collisions between the fighter and the platforms.

        INPUTS: {fighter} -> Fighter()
        OUTPUTS: ...
        """
        for platform in self.platforms:
            if fighter.rect.colliderect(platform) and fighter.vel_y > 0:
                fighter.rect.bottom = platform.top
                fighter.jumping = False
                fighter.vel_y = 0

    def draw(self, screen):
        for platform in self.platforms:
            pygame.draw.rect(screen, (150, 150, 150), platform)
