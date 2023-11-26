import pygame
import sys


# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 5
        self.jump_count = 10
        self.is_jumping = False

    def move_left(self):
        self.x -= self.speed

    def move_right(self):
        self.x += self.speed

    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True

    def update(self):
        if self.is_jumping:
            if self.jump_count >= -10:
                neg = 1
                if self.jump_count < 0:
                    neg = -1
                self.y -= (self.jump_count**2) * 0.5 * neg
                self.jump_count -= 1
            else:
                self.is_jumping = False
                self.jump_count = 10


def core_game_loop(
    screen: pygame.surface.Surface, clock: pygame.time.Clock, player: Player
) -> None:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Handle user input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.x > 0:
        player.move_left()
    if keys[pygame.K_RIGHT] and player.x < WIDTH - 50:
        player.move_right()
    if keys[pygame.K_SPACE]:
        player.jump()

    # Update game state
    player.update()

    # Render graphics
    screen.fill(WHITE)
    pygame.draw.rect(
        screen, BLACK, (player.x, player.y, 50, 50)
    )  # Placeholder for the player

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)


def main():
    # Initialize Pygame
    pygame.init()

    # Create the game window
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    print(type(screen))
    pygame.display.set_caption("Jump and Run Game")

    clock = pygame.time.Clock()

    player = Player(50, HEIGHT - 100)

    while True:
        core_game_loop(screen, clock, player)


if __name__ == "__main__":
    main()
