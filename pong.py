import pygame
from typing import Tuple, List

_rgb = Tuple[int, int, int]

pygame.init()

WIDTH, HEIGHT = 700, 500
WIN: pygame.Surface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

FPS: int = 60

WHITE: _rgb = (255, 255, 255)
BLACK: _rgb = (0, 0, 0)

PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_RADIUS: int = 7

SCORE_FONT: pygame.font.Font = pygame.font.SysFont("comicsans", 50)
WINNING_SCORE: int = 10


class Paddle:
    COLOR: _rgb = WHITE
    VEL: int = 4

    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        self._x = self._original_x = x
        self._y = self._original_y = y
        self._width: int = width
        self._height: int = height

    def draw(self, win: pygame.Surface) -> None:
        pygame.draw.rect(
            win, self.COLOR, (self._x, self._y, self._width, self.height))

    def move(self, up: bool= True) -> None:
        if up:
            self._y -= self.VEL
        else:
            self._y += self.VEL

    def reset(self) -> None:
        self._x = self._original_x
        self._y = self._original_y


class Ball:
    MAX_VEL: int = 5
    COLOR: _rgb = WHITE

    def __init__(self, x: int, y: int, radius: int) -> None:
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius: int = radius
        self.x_vel: int = self.MAX_VEL
        self.y_vel: int = 0

    def draw(self, win: pygame.Surface) -> None:
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)

    def move(self) -> None:
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self) -> None:
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel = 0
        self.x_vel *= -1


def draw(win: pygame.Surface, paddles: List[Paddle], ball: Ball, left_score: int, right_score: int) -> None:
    win.fill(BLACK)

    left_score_text: pygame.Surface = SCORE_FONT.render(f"{left_score}", 1, WHITE)
    right_score_text: pygame.Surface = SCORE_FONT.render(f"{right_score}", 1, WHITE)
    win.blit(left_score_text, (WIDTH//4 - left_score_text.get_width()//2, 20))
    win.blit(right_score_text, (WIDTH * (3/4) -
                                right_score_text.get_width()//2, 20))

    for paddle in paddles:
        paddle.draw(win)

    for i in range(10, HEIGHT, HEIGHT//20):
        if i % 2 == 1:
            continue
        pygame.draw.rect(win, WHITE, (WIDTH//2 - 5, i, 10, HEIGHT//20))

    ball.draw(win)
    pygame.display.update()


def handle_collision(ball: Ball, left_paddle: Paddle, right_paddle: Paddle) -> None:
    ball_below_bottom = ball.y + ball.radius >= HEIGHT
    ball_above_top = ball.y - ball.radius <= 0

    if ball_below_bottom:
        ball.y_vel *= -1
    elif ball_above_top:
        ball.y_vel *= -1

    ball_moving_left = ball.x_vel < 0

    if ball_moving_left:
        ball_between_left_paddle_y: bool = ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height
        ball_exceeds_left_x: bool = ball.x - ball.radius <= left_paddle.x + left_paddle.width

        if ball_between_left_paddle_y:
            if ball_exceeds_left_x:
                ball.x_vel *= -1

                middle_y: float = left_paddle.y + left_paddle.height / 2
                difference_in_y: float = middle_y - ball.y
                reduction_factor: float = (left_paddle.height / 2) / ball.MAX_VEL
                y_vel: float = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel

    else:
        ball_between_right_paddle_y: bool = ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height
        ball_exceeds_right_x: bool = ball.x + ball.radius >= right_paddle.x

        if ball_between_right_paddle_y:
            if ball_exceeds_right_x:
                ball.x_vel *= -1

                middle_y: float = right_paddle.y + right_paddle.height / 2
                difference_in_y: float = middle_y - ball.y
                reduction_factor: float = (right_paddle.height / 2) / ball.MAX_VEL
                y_vel: float = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel


def handle_paddle_movement(keys: pygame.key.ScancodeWrapper, left_paddle: Paddle, right_paddle: Paddle) -> None:

    # conditions
    pressed_W: bool = keys[pygame.K_w]
    pressed_S: bool = keys[pygame.K_w]
    pressed_UP: bool = keys[pygame.K_w]
    pressed_DOWN: bool = keys[pygame.K_w]
    left_paddle_below_top_bound: bool = left_paddle.y - left_paddle.VEL >= 0
    left_paddle_above_bottom_bound: bool = left_paddle.y + left_paddle.VEL + left_paddle.height <= HEIGHT
    right_paddle_below_top_bound: bool = right_paddle.y - right_paddle.VEL >= 0
    right_paddle_above_bottom_bound: bool = right_paddle.y + right_paddle.VEL + right_paddle.height <= HEIGHT

    if pressed_W and left_paddle_below_top_bound:
        left_paddle.move(up=True)
    if pressed_S and left_paddle_above_bottom_bound:
        left_paddle.move(up=False)

    if pressed_UP and right_paddle_below_top_bound:
        right_paddle.move(up=True)
    if pressed_DOWN and right_paddle_above_bottom_bound:
        right_paddle.move(up=False)


def main() -> None:
    run = True
    clock: pygame.time.Clock = pygame.time.Clock()

    left_paddle: Paddle = Paddle(10, HEIGHT//2 - PADDLE_HEIGHT //
                         2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle: Paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT //
                          2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball: Ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS)

    left_score: int = 0
    right_score: int = 0

    while run:
        clock.tick(FPS)
        draw(WIN, [left_paddle, right_paddle], ball, left_score, right_score)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys: pygame.key.ScancodeWrapper = pygame.key.get_pressed()
        handle_paddle_movement(keys, left_paddle, right_paddle)

        ball.move()
        handle_collision(ball, left_paddle, right_paddle)

        left_misses_ball: bool = ball.x < 0
        right_misses_ball: bool = ball.x > WIDTH

        if left_misses_ball:
            right_score += 1
            ball.reset()
        elif right_misses_ball:
            left_score += 1
            ball.reset()

        won: bool = False
        if left_score >= WINNING_SCORE:
            won = True
            win_text = "Left Player Won!"
        elif right_score >= WINNING_SCORE:
            won = True
            win_text = "Right Player Won!"

        if won:
            text: pygame.Surface = SCORE_FONT.render(win_text, 1, WHITE)
            WIN.blit(text, (WIDTH//2 - text.get_width() //
                            2, HEIGHT//2 - text.get_height()//2))
            pygame.display.update()
            pygame.time.delay(5000)
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            left_score = 0
            right_score = 0

    pygame.quit()


if __name__ == '__main__':
    main()