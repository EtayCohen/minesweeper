import random
import argparse

HEIGHT = 7
WIDTH = 7
BOMBS = 4


class Cell:
    def __init__(self, r, c, m, n):
        self.r = r
        self.c = c
        self.m = m
        self.n = n
        self.value = 0
        self.revealed = False
        self.bomb = False
        self.flg = False

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
    def __init__(self, m, n, bombs):
        self.grid = [[Cell(r, c, m, n) for c in range(n)] for r in range(m)]
        self.m = m
        self.n = n
        self.bombs = bombs
        self.set_bombs()
        self.set_values()
        self.flags = 0

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
            print("please enter values withing range")
            return True
        cell = self.grid[r][c]
        if op == 'f':
            self.flags += -1 if cell.flg else 1
            self.grid[r][c].flag()
        elif cell.flg:
            pass
        elif cell.bomb:
            print("GAME OVER")
            self.reveal_grid()
            return False
        self.grid[r][c].reveal(self.grid)
        return True

    def __str__(self):
        s = ""
        for row in self.grid:
            for cell in row:
                s += f"{cell}{(5 - len(str(cell))) * ' '}"
            s += "\n"
        return s


def main():
    g = Grid(HEIGHT, WIDTH, BOMBS)
    while g.play_turn(input("flag / reveal ->"), input("row -> "), input("col -> ")):
        print(g.bombs_status())
        print(g)
    print(g)


if __name__ == '__main__':
    main()
