import random
import pygame
from pygame.locals import *
import argparse

HEIGHT = 640

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

REVEAL = 1

pygame.init()
pygame.font.init()

FONT = pygame.font.Font('freesansbold.ttf', 32)


class Cell:
    def __init__(self, r, c, m, n, block_size):
        self.r = r
        self.c = c
        self.m = m
        self.n = n
        self.value = 0
        self.revealed = False
        self.bomb = False
        self.flg = False
        self.block_size = block_size

    def set_value(self, grid):
        s = 0
        if self.bomb:
            return
        for r in range(-1, 2):
            i = self.r + r
            if i < 0 or i >= self.m:
                continue
            for c in range(-1, 2):
                j = self.c + c
                if 0 <= j < self.n and grid[i][j].bomb:
                    s += 1
        self.value = s

    def flag(self):
        self.flg = not self.flg
        self.revealed = self.flg

    def reveal(self, grid):
        self.revealed = True
        if not self.bomb and self.value == 0:
            self.flood(grid)

    def draw(self, screen):
        r = pygame.Rect(self.c * self.block_size, self.r *
                        self.block_size, self.block_size, self.block_size)
        pygame.draw.rect(screen, (0, 0, 0), r, 2)
        t = FONT.render(str(self), False, BLACK)
        r = t.get_rect()
        r.center = (self.c * self.block_size + 0.5 * self.block_size,
                    self.r * self.block_size + 0.5 * self.block_size)

        screen.blit(t, r)

    def flood(self, grid):
        for r in range(-1, 2):
            i = self.r + r
            if i < 0 or i >= self.m:
                continue
            for c in range(-1, 2):
                j = self.c + c
                if 0 <= j < self.n and not grid[i][j].revealed:
                    grid[i][j].reveal(grid)

    def __str__(self):
        return ("F" if self.flg else ("X" if self.bomb else str(self.value))) if self.revealed else "?"


class Grid:
    def __init__(self, m, n, bombs, block_size):
        self.grid = [[Cell(r, c, m, n, block_size)
                      for c in range(n)] for r in range(m)]
        self.m = m
        self.n = n
        self.bombs = bombs
        self.set_bombs()
        self.set_values()
        self.flags = 0
        self.block_size = block_size

    def set_values(self):
        for r in self.grid:
            for cell in r:
                cell.set_value(self.grid)

    def set_bombs(self):
        options = [(r, c) for r in range(self.m) for c in range(self.n)]
        for _ in range(self.bombs):
            r, c = random.choice(options)
            self.grid[r][c].bomb = True
            options.remove((r, c))

    def reveal_grid(self):
        for row in self.grid:
            for cell in row:
                if cell.flg:
                    cell.flag()
                cell.revealed = True

    def bombs_status(self):
        return self.bombs - self.flags

    def play_turn(self, op, r, c):
        r, c = int(r), int(c)
        if r >= self.m or c >= self.n:
            return True
        cell = self.grid[r][c]
        if op != REVEAL:
            self.flags += -1 if cell.flg else 1
            self.grid[r][c].flag()
        elif cell.flg:
            pass
        elif cell.bomb:
            self.reveal_grid()
            return False
        self.grid[r][c].reveal(self.grid)
        return True

    def draw(self, screen):
        for r in range(self.m):
            for c in range(self.n):
                self.grid[r][c].draw(screen)

        t = FONT.render(str(self.bombs_status()), False, BLACK)
        r = t.get_rect()
        r.center = ((self.n * self.block_size)/2,
                    self.m * self.block_size + (HEIGHT - self.m * self.block_size)/2)
        screen.blit(t, r)

    def __str__(self):
        s = ""
        for row in self.grid:
            for cell in row:
                s += f"{cell}{(5 - len(str(cell))) * ' '}"
            s += "\n"
        return s


def main():
    m, n, bombs = 10, 12, 7
    block_size = int((HEIGHT - 50) / m)

    g = Grid(m, n, bombs, block_size)
    screen = pygame.display.set_mode((n*block_size, HEIGHT))
    pygame.display.set_caption('MINESWEEPER')
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                c, r = pygame.mouse.get_pos()
                g.play_turn(event.button, r / block_size, c / block_size)
        screen.fill(WHITE)
        g.draw(screen)
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main()
