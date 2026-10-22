
import pygame
from game.game_engine import GameEngine

pygame.init()

WIDTH, HEIGHT = 600, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake - Pygame Version")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

clock = pygame.time.Clock()
FPS = 60

DIFFICULTIES = {
    pygame.K_1: ("Easy", 5),
    pygame.K_2: ("Medium", 8),
    pygame.K_3: ("Hard", 14),
}


def create_engine(speed=8):
    engine = GameEngine(WIDTH, HEIGHT)
    engine.moves_per_second = speed
    return engine


def main():
    running = True
    engine = create_engine()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if engine.game_over:
                    if event.key == pygame.K_ESCAPE:
                        running = False

                    elif event.key in DIFFICULTIES:
                        _, speed = DIFFICULTIES[event.key]
                        engine = create_engine(speed)

                else:
                    engine.handle_keydown(event.key)

        if not running:
            break

        engine.handle_input()
        engine.update()
        engine.render(SCREEN)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
