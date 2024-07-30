# Bomberman-Inspired Game

This project is a Bomberman-inspired game developed using Python and the Pygame library. It features both single-player and multiplayer modes, with dynamic map selection and different map variations. The game offers a grid-based layout where players navigate characters through various obstacles, enemies, and destructible blocks. The objective is to strategically place bombs to eliminate enemies and clear a path through the maze-like levels.

## New Features

- **Multiplayer Mode:** Compete head-to-head with another player, navigating the grid, planting bombs, and strategically outmaneuvering your opponent.
- **Map Selection and Variations:** Choose from different maps or load custom maps, enhancing the gameplay experience.
- **Enhanced AI:** AI-controlled enemies use Depth-First Search (DFS) and Dijkstra's algorithms for more challenging gameplay.

## Original Source

This project builds upon the work from the original repository: [Forestf90/Bomberman](https://github.com/Forestf90/Bomberman). The additional features such as multiplayer mode, map selection, and different map variations were added to expand the original game's capabilities.

## Installation

To install the necessary dependencies, run the following commands:

```bash
pip3 install pygame
pip3 install pygame-menu
```

## Running the Game

Navigate to the main directory and execute the following command to start the game:

```bash
cd..
python3 -m bomberman_2d.src.menu
```

## Running Tests

```bash
cd..
python3 -m unittest bomberman_2d/tests/map_generation_test.py
python3 -m unittest bomberman_2d/tests/bomb_test.py
python3 -m unittest bomberman_2d/tests/explosion_test.py
```

## Controls

### Single-Player

- **Movement:** Arrow keys
- **Plant Bomb:** Spacebar

### Multi-Player

- **Player 1:**
  - **Movement:** "WASD" keys
  - **Plant Bomb:** "E" key
- **Player 2:**
  - **Movement:** Arrow keys
  - **Plant Bomb:** Spacebar

## Selecting a Custom Map

To select a custom map, navigate to `Start` --> `Options` --> `Mapfile`. Enter the name of the map file without the relative path or extension, for example, `no_walls` or `all_walls`.

