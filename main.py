import pygame
from fighter import Fighter
from powerup import PowerUp
from arena import Arena
import random

pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('PIXEL PUNCH')

bg_image = pygame.image.load("background.jpeg")
bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

font = pygame.font.Font('actioncomics.ttf', 36)
title_text = font.render('PIXEL PUNCH', True, (255, 255, 255))
start_text = font.render('PRESS ENTER', True, (255, 255, 255))

player1 = Fighter(1, SCREEN_WIDTH * 0.25, SCREEN_HEIGHT - 190, 'player1.png')
player2 = Fighter(2, SCREEN_WIDTH * 0.75, SCREEN_HEIGHT - 190, 'player2.png')

arena = Arena()

powerups = []

clock = pygame.time.Clock()
running = True
in_start_page = True

spawn_timer = 300

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        player1.handle_event(event, player2)
        player2.handle_event(event, player1)

    keys = pygame.key.get_pressed()

    if in_start_page:
        if keys[pygame.K_RETURN]:
            in_start_page = False
        screen.blit(bg_image, (0, 0))
        screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, SCREEN_HEIGHT//4))
        screen.blit(start_text, (SCREEN_WIDTH//2 - start_text.get_width()//2, SCREEN_HEIGHT//2))
    else:
        # Movement
        player1.move(keys)
        player2.move(keys)

        # Draw
        screen.blit(bg_image, (0, 0))
        arena.draw(screen)
        player1.draw(screen)
        player1.draw_health_bar(screen)
        player2.draw(screen)
        player2.draw_health_bar(screen)

        for powerup in powerups:
            powerup.draw(screen)

        # Check win condition
        if player1.health <= 0:
            print("Player 2 wins!")
            running = False
        elif player2.health <= 0:
            print("Player 1 wins!")
            running = False

        # Arena collisions
        arena.check_collisions(player1)
        arena.check_collisions(player2)

        # Powerup mechanism
        spawn_timer -= 1
        if spawn_timer <= 0:
            powerups.append(PowerUp())
            spawn_timer = random.randint(200, 400)

        for powerup in powerups:
            if player1.rect.colliderect(powerup.rect):
                powerup.apply(player1)
                powerups.remove(powerup)
            elif player2.rect.colliderect(powerup.rect):
                powerup.apply(player2)
                powerups.remove(powerup)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
