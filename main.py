import random
import pygame
from pygame.locals import *
import argparse

HEIGHT = 640
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
REVEAL = 1
BOTTOM_PADDING = 50

pygame.init()
pygame.font.init()

FONT = pygame.font.Font('freesansbold.ttf', 30)


class Cell:
    def __init__(self, r, c, m, n, block_size):
        """
        :param r: row index
        :param c: col index
        :param m: rows
        :param n: cols
        :param block_size: block size
        """
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
        """
        Counts surrounding bombs and sets cell's value
        :param grid: game's grid
        :return: None
        """
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
        """
        Flags and unflags cell
        :return: None
        """
        self.flg = not self.flg
        self.revealed = self.flg

    def reveal(self, grid):
        """
        Reveals cell
        :param grid: game's grid
        :return: None
        """
        self.revealed = True
        if not self.bomb and self.value == 0:
            self.flood(grid)

    def draw(self, screen):
        """
        Draws cell on screen
        :param screen: screen to draw on
        :return: None
        """
        r = pygame.Rect(self.c * self.block_size, self.r *
                        self.block_size, self.block_size, self.block_size)
        pygame.draw.rect(screen, (0, 0, 0), r, 2)
        t = FONT.render(str(self), False, BLACK)
        r = t.get_rect()
        r.center = (self.c * self.block_size + 0.5 * self.block_size,
                    self.r * self.block_size + 0.5 * self.block_size)

        screen.blit(t, r)

    def flood(self, grid):
        """
        Floods grid
        :param grid: game's grid
        :return: None
        """
        for r in range(-1, 2):
            i = self.r + r
            if i < 0 or i >= self.m:
                continue
            for c in range(-1, 2):
                j = self.c + c
                if 0 <= j < self.n and not grid[i][j].revealed:
                    grid[i][j].reveal(grid)

    def __str__(self):
        """
        Returns object as string
        :return: object as string
        """
        return ("F" if self.flg else ("X" if self.bomb else str(self.value))) if self.revealed else "?"


class Grid:
    def __init__(self, m, n, bombs, block_size):
        """
        :param m: rows
        :param n: cols
        :param bombs: bombs count
        :param block_size: block size
        """
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
        """
        Sets cells values
        :return: None
        """
        for r in self.grid:
            for cell in r:
                cell.set_value(self.grid)

    def set_bombs(self):
        """
        Randomly places bombs
        :return: None
        """
        options = [(r, c) for r in range(self.m) for c in range(self.n)]
        for _ in range(self.bombs):
            r, c = random.choice(options)
            self.grid[r][c].bomb = True
            options.remove((r, c))

    def reveal_grid(self):
        """
        Reveals all cells
        :return: None
        """
        for row in self.grid:
            for cell in row:
                if cell.flg:
                    cell.flag()
                cell.revealed = True

    def bombs_status(self):
        """
        Returns how many bombs left to flag
        :return: bombs left to flag
        """
        return self.bombs - self.flags

    def is_won(self):
        """
        Checks whether in winning position
        :return: whether in winning position
        """
        if self.bombs_status() == 0:
            for row in self.grid:
                for c in row:
                    if not c.revealed:
                        return False
            return True
        return False

    def play_turn(self, op, r, c):
        """
        Plays a turn
        :param op: operation type
        :param r: row index
        :param c: col index
        :return: whether game ended and message to display
        """
        r, c = int(r), int(c)
        if r >= self.m or c >= self.n:
            return True, self.bombs_status()

        cell = self.grid[r][c]
        if op != REVEAL and (cell.flg or not cell.revealed):
            self.flags += -1 if cell.flg else 1
            self.grid[r][c].flag()
            if self.is_won():
                return False, "YOU WON"
            return True, self.bombs_status()

        if cell.flg:
            pass
        elif cell.bomb:
            self.reveal_grid()
            return False, "YOU LOST"

        self.grid[r][c].reveal(self.grid)
        if self.is_won():
            return False, "YOU WON"
        return True, self.bombs_status()

    def draw(self, screen):
        """
        Draws cells on screen
        :param screen: screen to draw on
        :return: None
        """
        for r in range(self.m):
            for c in range(self.n):
                self.grid[r][c].draw(screen)

    def __str__(self):
        """
        Returns object as string
        :return: object as string
        """
        s = ""
        for row in self.grid:
            for cell in row:
                s += f"{cell}{(5 - len(str(cell))) * ' '}"
            s += "\n"
        return s


def message(screen, m, n, block_size, msg):
    """
    Write message to screen
    :param screen: screen to write on
    :param m: rows
    :param n: cols
    :param block_size: block size
    :param msg: message to write
    :return: None
    """
    t = FONT.render(str(msg), False, BLACK)
    r = t.get_rect()
    r.center = ((n * block_size)/2,
                m * block_size + (HEIGHT - m * block_size)/2)
    screen.blit(t, r)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--height', type=int, required=True)
    parser.add_argument('--width', type=int, required=True)
    parser.add_argument('--bombs', type=int, required=True)
    args = parser.parse_args()

    m, n, bombs = args.height, args.width, args.bombs
    block_size = (HEIGHT - BOTTOM_PADDING) // m

    screen = pygame.display.set_mode((n*block_size, HEIGHT))
    pygame.display.set_caption('MINESWEEPER')

    msg = ""
    g = Grid(m, n, bombs, block_size)
    status, running = True, True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == K_BACKSPACE:
                g = Grid(m, n, bombs, block_size)
                msg = g.bombs_status()
                status = True
            elif status and event.type == pygame.MOUSEBUTTONUP:
                c, r = pygame.mouse.get_pos()
                status, msg = g.play_turn(
                    event.button, r / block_size, c / block_size)
        screen.fill(WHITE)
        g.draw(screen)
        message(screen, m, n, block_size, msg)
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main()
