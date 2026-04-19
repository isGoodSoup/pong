import os
import sys
import pygame

pygame.init()

FPS = 60
SCREEN_SIZE = pygame.display.Info().current_w, pygame.display.Info().current_h
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
CENTER = SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2
START_Y = SCREEN_SIZE[1] // 2
OFFSET = 100
pygame.mouse.set_visible(False)

def resource_path(path):
    if hasattr(sys, "_MEIPASS"):
        absolute_path = os.path.join(sys._MEIPASS, path)
    else:
        absolute_path = os.path.join(path)
    return absolute_path

def _play_(sound):
    sound.play()

sounds = [
    pygame.mixer.Sound(resource_path("assets/fx/hit.ogg")),
]

for sound in sounds:
    sound.set_volume(0.8)

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 100))
        self.image.fill(COLOR_WHITE)
        self.rect = self.image.get_rect(center=(x, y))
        self.score = 0

    def clamp_paddle(self):
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_SIZE[1]:
            self.rect.bottom = SCREEN_SIZE[1]

    def update(self):
        self.clamp_paddle()

class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(self.image, COLOR_WHITE, (10, 10), 10)

        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 15
        self.dx = self.dy = self.speed

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_SIZE[1]:
            self.dy *= -1
            _play_(sounds[0])

class Score:
    def __init__(self):
        self.font = pygame.font.Font(None, 36)

    def draw(self, screen, p1, p2):
        text = f"{p1.score}  |  {p2.score}"
        render = self.font.render(text, True, COLOR_WHITE)
        screen.blit(render, (SCREEN_SIZE[0] // 2 - render.get_width() // 2, 100))

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode(SCREEN_SIZE, vsync=1)
        self.clock = pygame.time.Clock()
        self.running = True

        pygame.display.set_caption("Pong")

        self.player1 = Player(OFFSET, START_Y)
        self.player2 = Player(SCREEN_SIZE[0] - OFFSET, START_Y)
        self.ball = pygame.sprite.GroupSingle(Ball(*CENTER))

        self.players = pygame.sprite.Group(self.player1, self.player2)
        self.speed = 15

        self.score = Score()

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

    def check_collision(self):
        ball = self.ball.sprite

        for player in self.players:
            if pygame.sprite.collide_rect(player, ball):
                ball.dx *= -1
                offset = (ball.rect.centery - player.rect.centery) / 50
                ball.dy = offset * 5
                _play_(sounds[0])

                if ball.dx > 0:
                    ball.rect.left = player.rect.right
                else:
                    ball.rect.right = player.rect.left

    def _check_goal_(self):
        ball = self.ball.sprite

        if ball.rect.left <= 0:
            self.player2.score += 1
            self._reset_ball_()

        if ball.rect.right >= SCREEN_SIZE[0]:
            self.player1.score += 1
            self._reset_ball_()

    def _reset_ball_(self):
        ball = self.ball.sprite
        ball.rect.center = CENTER
        ball.dx *= -1
        ball.dy = ball.speed

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill(COLOR_BLACK)
            self.clock.tick(FPS)
            self._input_()

            self.players.update()
            self.ball.update()
            self.check_collision()
            self._check_goal_()

            self.players.draw(self.screen)
            self.ball.draw(self.screen)
            self.score.draw(self.screen, self.player1, self.player2)

            pygame.display.flip()

        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    Game().run()
