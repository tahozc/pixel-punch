import pygame

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

class Fighter:
    def __init__(self, player, x, y, image_file):
        self.player = player
        self.image = pygame.image.load(image_file)
        self.image = pygame.transform.scale(self.image, (100, 180))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.vel_x = 0
        self.vel_y = 0
        self.jumping = False
        self.health = 100

    def draw_health_bar(self, screen):
        # Variables for the health bar's size and position
        BAR_WIDTH, BAR_HEIGHT = 100, 15
        OFFSET_Y = -20
        BORDER_THICKNESS = 2

        # Outer health bar (border)
        border_rect = pygame.Rect(self.rect.x, self.rect.y + OFFSET_Y, BAR_WIDTH, BAR_HEIGHT)
        pygame.draw.rect(screen, (255, 255, 255), border_rect)

        # Inner health bar
        inner_rect_width = BAR_WIDTH - (2 * BORDER_THICKNESS)
        health_rect_width = int(inner_rect_width * (self.health / 100))
        health_rect = pygame.Rect(self.rect.x + BORDER_THICKNESS, self.rect.y + OFFSET_Y + BORDER_THICKNESS, health_rect_width, BAR_HEIGHT - (2 * BORDER_THICKNESS))
        pygame.draw.rect(screen, (0, 255, 0), health_rect)  # Color changed to green

    def handle_event(self, event, opponent):
        # Basic attack mechanism (deducts health if in range/hitbox)
        ATTACK_DISTANCE = 50
        if self.player == 1 and event.type == pygame.KEYDOWN and event.key == pygame.K_s:
            if abs(self.rect.centerx - opponent.rect.centerx) < ATTACK_DISTANCE:
                opponent.health -= 10
        elif self.player == 2 and event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            if abs(self.rect.centerx - opponent.rect.centerx) < ATTACK_DISTANCE:
                opponent.health -= 10

    def move(self, keys):
        GRAVITY = 1
        SPEED = 5
        JUMP_STRENGTH = -15
        
        # Movement logic for Player 1
        if self.player == 1:
            if keys[pygame.K_a]:
                self.vel_x = -SPEED
            elif keys[pygame.K_d]:
                self.vel_x = SPEED
            else:
                self.vel_x = 0

            if keys[pygame.K_w] and not self.jumping:
                self.vel_y = JUMP_STRENGTH
                self.jumping = True
        
        # Movement logic for Player 2
        elif self.player == 2:
            if keys[pygame.K_LEFT]:
                self.vel_x = -SPEED
            elif keys[pygame.K_RIGHT]:
                self.vel_x = SPEED
            else:
                self.vel_x = 0

            if keys[pygame.K_UP] and not self.jumping:
                self.vel_y = JUMP_STRENGTH
                self.jumping = True

        # Apply gravity
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y

        # Ground collision
        if self.rect.y > SCREEN_HEIGHT - 190:
            self.rect.y = SCREEN_HEIGHT - 190
            self.jumping = False

        self.rect.x += self.vel_x

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
