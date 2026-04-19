import sys
import pygame

pygame.init()

FPS = 60
SCREEN_SIZE = pygame.display.Info().current_w, pygame.display.Info().current_h
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
START_Y = SCREEN_SIZE[1] // 2
OFFSET = 100

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 100))
        self.image.fill(COLOR_WHITE)
        self.rect = self.image.get_rect(center=(x, y))

    def clamp_paddle(self):
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_SIZE[1]:
            self.rect.bottom = SCREEN_SIZE[1]

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode(SCREEN_SIZE, vsync=1)
        self.clock = pygame.time.Clock()
        self.running = True

        pygame.display.set_caption("Pong")

        self.player1 = Player(OFFSET, START_Y)
        self.player2 = Player(SCREEN_SIZE[0] - OFFSET, START_Y)

        self.players = pygame.sprite.Group(self.player1, self.player2)
        self.speed = 8

    def _input_(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.player1.rect.y -= self.speed
        if keys[pygame.K_s]:
            self.player1.rect.y += self.speed

        if keys[pygame.K_UP]:
            self.player2.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.player2.rect.y += self.speed

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill(COLOR_BLACK)
            self.clock.tick(FPS)
            self._input_()
            self.player1.clamp_paddle()
            self.player2.clamp_paddle()
            self.players.update()
            self.players.draw(self.screen)
            pygame.display.flip()

        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    Game().run()
