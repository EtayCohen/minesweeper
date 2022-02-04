# Minesweeper

Minesweeper is a single-player puzzle video game. The objective of the game is to clear a rectangular board containing hidden "mines" or bombs without detonating any of them, with help from clues about the number of neighbouring mines in each field.

## Requirements

```sh
pip3 install -r requirements.txt
```

## Running

```sh
python3 main.py --height 10 --width 10 --bombs 7
```

## Playing

    - Reveal by left clicking
    - Flag by right clicking
    - Restart game by pressing backspace

## Implementation

    An object oriented implementation using [Pygame](https://www.pygame.org/) to create basic GUI
