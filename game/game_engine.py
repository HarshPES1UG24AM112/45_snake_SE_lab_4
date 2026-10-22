
import math
from array import array

import pygame
from .snake import Snake
from .food import Food

WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (220, 60, 60)
BLACK = (0, 0, 0)
YELLOW = (255, 220, 70)


class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cell_size = 20
        self.grid_width = width // self.cell_size
        self.grid_height = height // self.cell_size

        self.snake = Snake(
            self.grid_width // 2,
            self.grid_height // 2,
            self.cell_size,
        )
        self.food = Food(
            self.grid_width,
            self.grid_height,
            self.cell_size,
        )

        self.score = 0
        self.font = pygame.font.SysFont("Arial", 30)
        self.large_font = pygame.font.SysFont("Arial", 46, bold=True)
        self.small_font = pygame.font.SysFont("Arial", 22)

        self.moves_per_second = 8
        self._frame_counter = 0
        self._direction_changed = False

        self.game_over = False
        self._game_over_logged = False

        self.eat_sound = self._make_sound(700, 0.10)
        self.game_over_sound = self._make_sound(180, 0.35)

    def _make_sound(self, frequency, duration):
        """Create a simple sound effect without external sound files."""
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()

            sample_rate = 22050
            sample_count = int(sample_rate * duration)
            samples = array("h")

            for i in range(sample_count):
                fade = 1.0 - (i / sample_count)
                value = int(
                    9000
                    * fade
                    * math.sin(2 * math.pi * frequency * i / sample_rate)
                )
                samples.append(value)

            return pygame.mixer.Sound(buffer=samples.tobytes())
        except (pygame.error, OSError):
            return None

    def _play_sound(self, sound):
        if sound is not None:
            try:
                sound.play()
            except pygame.error:
                pass

    def handle_keydown(self, key):
        if self.game_over or self._direction_changed:
            return

        old_direction = self.snake.direction

        if key in (pygame.K_UP, pygame.K_w):
            self.snake.set_direction(0, -1)
        elif key in (pygame.K_DOWN, pygame.K_s):
            self.snake.set_direction(0, 1)
        elif key in (pygame.K_LEFT, pygame.K_a):
            self.snake.set_direction(-1, 0)
        elif key in (pygame.K_RIGHT, pygame.K_d):
            self.snake.set_direction(1, 0)

        if self.snake.direction != old_direction:
            self._direction_changed = True

    def handle_input(self):
        pass

    def _end_game(self):
        if not self.game_over:
            self.game_over = True
            self._play_sound(self.game_over_sound)

    def update(self):
        if self.game_over:
            return

        self._frame_counter += 1
        frames_per_move = max(1, 60 // self.moves_per_second)

        if self._frame_counter < frames_per_move:
            return

        self._frame_counter = 0
        self.snake.move()
        self._direction_changed = False

        if self.snake.collides_with_wall(
            self.grid_width, self.grid_height
        ):
            self._end_game()
            return

        if self.snake.collides_with_self():
            self._end_game()
            return

        if self.snake.head_rect().colliderect(self.food.rect()):
            self.snake.grow()
            self.score += 1
            self._play_sound(self.eat_sound)
            self.food.respawn(self.snake.body)

    def _draw_centered(self, screen, text, font, color, y):
        image = font.render(text, True, color)
        screen.blit(
            image,
            (self.width // 2 - image.get_width() // 2, y),
        )

    def render(self, screen):
        screen.fill(BLACK)

        pygame.draw.rect(screen, RED, self.food.rect())

        for rect in self.snake.segment_rects():
            pygame.draw.rect(screen, GREEN, rect)

        score_text = self.font.render(
            f"Score: {self.score}", True, WHITE
        )
        screen.blit(score_text, (10, 10))

        if self.game_over:
            overlay = pygame.Surface(
                (self.width, self.height), pygame.SRCALPHA
            )
            overlay.fill((0, 0, 0, 210))
            screen.blit(overlay, (0, 0))

            self._draw_centered(
                screen, "GAME OVER", self.large_font, RED, 170
            )
            self._draw_centered(
                screen,
                f"Final Score: {self.score}",
                self.font,
                WHITE,
                235,
            )
            self._draw_centered(
                screen, "Choose Difficulty", self.small_font, YELLOW, 300
            )
            self._draw_centered(
                screen, "1 - Easy", self.small_font, WHITE, 340
            )
            self._draw_centered(
                screen, "2 - Medium", self.small_font, WHITE, 375
            )
            self._draw_centered(
                screen, "3 - Hard", self.small_font, WHITE, 410
            )
            self._draw_centered(
                screen, "ESC - Exit", self.small_font, WHITE, 455
            )
