import pygame
from pygame.locals import *
import random

# Initialize pygame
pygame.init()

# Configuration
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
FPS = 60
WHITE = (255, 255, 255)
BACKGROUND_COLOR = (50, 50, 50)

# Fonts and pulsing effect
pixel_font_big = pygame.font.Font("ActionComics.ttf", 74)
pixel_font_small = pygame.font.Font("ActionComics.ttf", 24)

# Password configurations
password = ""
input_box = pygame.Rect(300, 300, 140, 40)
color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')
color = color_inactive
active = False
password_prompt_text = pixel_font_small.render('ENTER PASSWORD', True, WHITE)

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pixel Punch")
clock = pygame.time.Clock()

# Load sprites
player_sprites = [f'sprite{i}.png' for i in range(1, 4)]
all_sprites = [pygame.transform.scale(pygame.image.load(sprite_path).convert_alpha(), (100, 100)) for sprite_path in player_sprites]
selected_sprite_index = 0

class HealthBar:
    def __init__(self, x, y, player):
        self.x = x
        self.y = y
        self.player = player
        self.max_health = 10
        self.current_health = self.max_health
        self.width = 100
        self.height = 10
        self.ai_decision_delay = 30
        self.ai_decision_counter = 0

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y, self.width * (self.current_health / self.max_health), self.height))

    def reduce_health(self, damage):
        self.current_health -= damage
        if self.current_health < 0:
            self.current_health = 0

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, sprite, is_ai=False):
        super().__init__()

        self.image = sprite
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.change_x = 0
        self.change_y = 0
        self.gravity = 1
        self.ground = SCREEN_HEIGHT - self.rect.height
        self.is_jumping = False
        self.is_ai = is_ai
        self.last_ability_use = pygame.time.get_ticks()
        self.ability_cooldown = 5000  # 5000 milliseconds = 5 seconds
        
        # Add AI-related attributes here
        if self.is_ai:
            self.ai_decision_delay = 30
            self.ai_decision_counter = 0

    def can_use_ability(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_ability_use >= self.ability_cooldown:
            self.last_ability_use = current_time
            return True
        return False

    def damage_opponent(self, opponent):
        if self.can_use_ability():
            opponent.health_bar.reduce_health(1)

    def update(self):
        # Gravity effect and basic movement
        if self.rect.y < self.ground:
            self.change_y += self.gravity
        elif self.change_y > 0:
            self.is_jumping = False
            self.change_y = 0
            self.rect.y = self.ground
        self.rect.x += self.change_x
        self.rect.y += self.change_y

        # Basic AI for Player 2
        if self.is_ai:
            if self.ai_decision_counter == 0:
                if random.randint(0, 1) == 0:
                    if self.rect.x < player1.rect.x:
                        self.go_right()
                    else:
                        self.go_left()
                self.ai_decision_counter = self.ai_decision_delay
            else:
                self.ai_decision_counter -= 1
                
    def collide_with(self, other_player):
        if self.rect.colliderect(other_player.rect):
            dx = self.rect.centerx - other_player.rect.centerx
            dy = self.rect.centery - other_player.rect.centery

            if abs(dx) > abs(dy):
                if dx > 0:
                    self.rect.left = other_player.rect.right
                else:
                    self.rect.right = other_player.rect.left
            else:
                if self.rect.bottom > other_player.rect.bottom:
                    self.rect.bottom = other_player.rect.top
                    self.change_y = 0  # prevent further falling
                else:
                    self.rect.top = other_player.rect.bottom
                self.change_y = 0


    def invert_colors(self):
        inverted_image = pygame.Surface(self.image.get_size())
        pygame.surfarray.blit_array(inverted_image, 255 - pygame.surfarray.array3d(self.image))
        self.image = inverted_image.convert_alpha()
        pygame.time.set_timer(pygame.USEREVENT, 5000)

    def reset_colors(self, sprite_path):
        self.image = pygame.transform.scale(pygame.image.load(sprite_path).convert_alpha(), (100, 100))

    def go_left(self): 
        self.change_x = -5

    def go_right(self): 
        self.change_x = 5

    def stop(self): 
        self.change_x = 0

    def jump(self):
        if self.rect.y == self.ground:
            self.change_y = -15


# screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# pygame.display.set_caption("Pixel Punch")
# clock = pygame.time.Clock()

# Setup Players and HealthBars
player1 = Player(100, SCREEN_HEIGHT - 100, all_sprites[0])
player2 = Player(700, SCREEN_HEIGHT - 100, all_sprites[1], is_ai=True)
player1_health_bar = HealthBar(50, 50, player1)
player2_health_bar = HealthBar(SCREEN_WIDTH - 150, 50, player2)
player1.health_bar = player1_health_bar
player2.health_bar = player2_health_bar

state = "START_PAGE"
pulse_title_text = None
current_font_size = 70
pulse_direction = 1
min_font_size = 70
max_font_size = 78

# Main game loop
running = True
while running:
    screen.fill(BACKGROUND_COLOR)

    # Handling for the start page
    if state == "START_PAGE":
        if current_font_size > max_font_size or current_font_size < min_font_size:
            pulse_direction *= -1
        if pulse_direction == 1 and current_font_size == min_font_size:
            pulse_font = pygame.font.Font("ActionComics.ttf", current_font_size)
        if pulse_direction == -1 and current_font_size == max_font_size:
            pulse_font = pygame.font.Font("ActionComics.ttf", current_font_size)
        current_font_size += pulse_direction
        pulse_title_text = pulse_font.render('PIXEL PUNCH', True, (173, 216, 230))

        for event in pygame.event.get():
            if event.type == QUIT: running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        if password == "taha":
                            state = "CHARACTER_SELECT"
                            password = ""
                        else:
                            password = ""
                    elif event.key == pygame.K_BACKSPACE:
                        password = password[:-1]
                    else:
                        password += event.unicode

        screen.fill((50, 50, 50))
        screen.blit(pulse_title_text, (SCREEN_WIDTH // 2 - pulse_title_text.get_width() // 2, SCREEN_HEIGHT // 2 - 150))
        
        password_prompt_position_y = SCREEN_HEIGHT // 2 + 20  # Adjust this value if needed
        screen.blit(password_prompt_text, (SCREEN_WIDTH // 2 - password_prompt_text.get_width() // 2, password_prompt_position_y))
        
        input_box.topleft = (SCREEN_WIDTH // 2 - input_box.width // 2, password_prompt_position_y + password_prompt_text.get_height() + 10)
        
        txt_surface = pixel_font_small.render(password, True, color)
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, color, input_box, 2)

    # Handling for the character selection screen
    elif state == "CHARACTER_SELECT":
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_LEFT and selected_sprite_index > 0:
                    selected_sprite_index -= 1
                elif event.key == K_RIGHT and selected_sprite_index < len(all_sprites) - 1:
                    selected_sprite_index += 1
                elif event.key == K_RETURN:
                    chosen_sprite = all_sprites[selected_sprite_index]
                    player1.image = chosen_sprite
                    state = "MAIN_GAME"

        # Drawing the sprites for selection
        for i, sprite in enumerate(all_sprites):
            position = (i * 110 + 100, SCREEN_HEIGHT // 2 - 50)
            screen.blit(sprite, position)
            if i == selected_sprite_index:
                pygame.draw.rect(screen, (255, 0, 0), (position[0]-5, position[1]-5, 110, 110), 5)  # Highlight the selected sprite with a red border


    # Handling for the main game
    elif state == "MAIN_GAME":
        for event in pygame.event.get():
            if event.type == QUIT: 
                running = False
            elif event.type == KEYDOWN:
                # Player 1 Controls
                if event.key == K_a: 
                    player1.go_left()
                elif event.key == K_d: 
                    player1.go_right()
                elif event.key == K_w: 
                    player1.jump()
                elif event.key == K_s: 
                    player1.damage_opponent(player2)  # Player 1 damages Player 2

                # Player 2 Controls (Human control)
                # if event.key == K_LEFT: player2.go_left()
                # elif event.key == K_RIGHT: player2.go_right()
                # elif event.key == K_UP: player2.jump()

            elif event.type == KEYUP:
                if event.key in [K_a, K_d]: 
                    player1.stop()
                elif event.key in [K_LEFT, K_RIGHT]: 
                    player2.stop()

            elif event.type == pygame.USEREVENT:
                player2.reset_colors(player_sprites[1])
        screen.fill(BACKGROUND_COLOR)

        # Player collision
        player1.collide_with(player2)
        player2.collide_with(player1)

        # Drawing and updating
        player1.update()
        player2.update()
        player1_health_bar.draw(screen)
        player2_health_bar.draw(screen)
        screen.blit(player1.image, player1.rect)
        screen.blit(player2.image, player2.rect)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()

