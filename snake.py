import random
import time
import os
import sys
import curses
from curses import wrapper
import numpy as np

class SnakeGame:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.stdscr.clear()
        self.height, self.width = self.stdscr.getmaxyx()
        self.snake = [(self.height//2, self.width//2)]
        self.direction = curses.KEY_RIGHT
        self.food = self.generate_food()
        self.game_over = False
        self.score = 0
        self.stdscr.timeout(100)
        self.stdscr.keypad(True)
        curses.curs_set(0)
        self.stdscr.border()
        self.draw()

    def draw(self):
        self.stdscr.clear()
        self.stdscr.border()
        self.stdscr.addch(self.food[0], self.food[1], '*')
        for y, x in self.snake:
            self.stdscr.addch(y, x, '#')
        score_text = f"Score: {self.score}"
        self.stdscr.addstr(self.height-1, 1, score_text)

    def generate_food(self):
        while True:
            y = random.randint(1, self.height-2)
            x = random.randint(1, self.width-2)
            if (y, x) not in self.snake:
                return y, x

    def move(self):
        head = self.snake[0]
        if self.direction == curses.KEY_UP:
            new_head = ((head[0] - 1) % self.height, head[1])
        elif self.direction == curses.KEY_DOWN:
            new_head = ((head[0] + 1) % self.height, head[1])
        elif self.direction == curses.KEY_LEFT:
            new_head = (head[0], (head[1] - 1) % self.width)
        elif self.direction == curses.KEY_RIGHT:
            new_head = (head[0], (head[1] + 1) % self.width)
        else:
            raise ValueError(f"Invalid direction: {self.direction}")

        if new_head in self.snake:
            self.game_over = True
            return

        self.snake.insert(0, new_head)
        if new_head == self.food:
            self.score += 1
            self.food = self.generate_food()
        else:
            self.snake.pop()

    def handle_input(self):
        key = self.stdscr.getch()
        if key in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT]:
            self.direction = key
        elif key == ord('q'):
            self.game_over = True

    def run(self):
        while not self.game_over:
            self.draw()
            self.handle_input()
            self.move()
            self.stdscr.refresh()
        msg = "Game Over! Press any key to exit..."
        self.stdscr.addstr(self.height // 2, max(0, self.width // 2 - len(msg) // 2), msg, curses.A_BOLD)
        self.stdscr.refresh()
        # 等待按任意键
        self.stdscr.nodelay(False)
        self.stdscr.getch()

if __name__ == "__main__":
    wrapper(SnakeGame)
    sys.exit(0)