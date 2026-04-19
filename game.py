import sys

import pygame

pygame.init()

FPS = 60
SCREEN_SIZE = pygame.display.Info().current_w, pygame.display.Info().current_h
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
START_Y = SCREEN_SIZE[1] // 2

screen = pygame.display.set_mode(SCREEN_SIZE, vsync=1)
pygame.display.set_caption("Pong")
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 100))
        self.image.fill(COLOR_WHITE)
        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect(center=(x, y))

player1 = pygame.sprite.GroupSingle(Player(50, START_Y))
player2 = pygame.sprite.GroupSingle(Player(SCREEN_SIZE[0] - 50, START_Y))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(COLOR_BLACK)
    clock.tick(FPS)
    player1.draw(screen)
    player2.draw(screen)
    pygame.display.flip()

pygame.quit()
sys.exit()