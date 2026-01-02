import os
import random
import time
import sys
##ozzznake is the game created by ozzie for fun and learning purposes##
##guys life is short play these kind of silly game and live man ....for more fun dont forget to follow me and give this project some good amt of stars on github##
try:
    import msvcrt
    WINDOWS = True
except ImportError:
    WINDOWS = False

def get_key_non_windows():
    try:
        import tty, termios
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        tty.setraw(fd)
        ch = sys.stdin.read(1)
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
        return ch
    except:
        return input("Move (W/A/S/D): ").strip()[:1]

WIDTH, HEIGHT = 30, 15
FPS = 10

EMPTY = ' '
WALL = '#'
HEAD = 'O'
BODY = 'o'
BALL = '@'

DIRS = {
    'UP': (0, -1),
    'DOWN': (0, 1),
    'LEFT': (-1, 0),
    'RIGHT': (1, 0)
}

KEYMAP = {
    b'w': 'UP', b'W': 'UP',
    b's': 'DOWN', b'S': 'DOWN',
    b'a': 'LEFT', b'A': 'LEFT',
    b'd': 'RIGHT', b'D': 'RIGHT',
    b'H': 'UP',
    b'P': 'DOWN',
    b'K': 'LEFT',
    b'M': 'RIGHT'
}

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def make_board():
    board = [[EMPTY] * WIDTH for _ in range(HEIGHT)]
    for x in range(WIDTH):
        board[0][x] = WALL
        board[HEIGHT - 1][x] = WALL
    for y in range(HEIGHT):
        board[y][0] = WALL
        board[y][WIDTH - 1] = WALL
    return board

def place_ball(snake):
    while True:
        x = random.randint(1, WIDTH - 2)
        y = random.randint(1, HEIGHT - 2)
        if (x, y) not in snake:
            return (x, y)

def draw(board, snake, ball, score):
    canvas = [row[:] for row in board]
    bx, by = ball
    canvas[by][bx] = BALL
    hx, hy = snake[0]
    canvas[hy][hx] = HEAD
    for (x, y) in snake[1:]:
        canvas[y][x] = BODY
    clear()
    print(f"Snake Game | Score: {score}")
    for row in canvas:
        print(''.join(row))

def read_input(current_dir):
    if WINDOWS:
        if msvcrt.kbhit():
            ch = msvcrt.getch()
            if ch in (b'\x03', b'\x1b', b'q', b'Q'):
                return 'QUIT'
            if ch == b'\xe0' and msvcrt.kbhit():
                ch = msvcrt.getch()
            return KEYMAP.get(ch, current_dir)
        return current_dir
    else:
        return current_dir

def main():
    random.seed()
    board = make_board()
    start_x = WIDTH // 2
    start_y = HEIGHT // 2
    snake = [(start_x, start_y), (start_x - 1, start_y), (start_x - 2, start_y)]
    direction = 'RIGHT'
    ball = place_ball(snake)
    score = 0
    last_move = time.time()
    step_delay = 1.5 / FPS

    while True:
        if WINDOWS:
            new_dir = read_input(direction)
            if new_dir == 'QUIT':
                print("Bye!")
                break
            if new_dir in DIRS:
                nx, ny = DIRS[new_dir]
                cx, cy = DIRS[direction]
                if (nx, ny) != (-cx, -cy):
                    direction = new_dir

        now = time.time()
        if now - last_move >= step_delay:
            last_move = now
            dx, dy = DIRS[direction]
            hx, hy = snake[0]
            nx, ny = hx + dx, hy + dy

            if nx <= 0 or nx >= WIDTH - 1 or ny <= 0 or ny >= HEIGHT - 1 or (nx, ny) in snake:
                draw(board, snake, ball, score)
                print("Game Over!")
                print(f"Final Score: {score}")
                break

            snake.insert(0, (nx, ny))
            if (nx, ny) == ball:
                score += 1
                ball = place_ball(snake)
            else:
                snake.pop()

            draw(board, snake, ball, score)

        time.sleep(0.005)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
