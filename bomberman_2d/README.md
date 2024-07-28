## Description

I am working on a Bomberman-inspired game in Python using the Pygame library. The game features a grid-based layout where the player navigates a character through various obstacles, enemies, and destructible blocks. The objective is to strategically place bombs to eliminate enemies and clear a path through the maze-like levels.

The player controls a character that can move horizontally and vertically across the grid. The movement is implemented with smoothening to enhance the player's experience. The character has the ability to plant bombs, each with a blast radius and the potential to destroy obstacles and enemies.

The game includes different power-ups that the player can collect, enhancing their abilities. These power-ups include increased bomb limit, extended blast radius, and other bonuses. Additionally, enemies move throughout the grid, posing a threat to the player. The player needs to outmaneuver the enemies and strategically use bombs to eliminate them.

In addition to the previously described features, the game offers both single-player and multiplayer.

In the single-player mode, players engage in challenging gameplay against AI-controlled enemies. The enemies utilize two different algorithms—Depth-First Search (DFS) and Dijkstra's algorithm—to navigate the grid, adding strategic depth and variety to the gameplay. Players must outwit these AI opponents while navigating the maze, planting bombs, and collecting power-ups to enhance their chances of success.

In multiplayer mode, two participants can compete head-to-head, navigating the grid, planting bombs, and strategically attempting to outmaneuver each other. This adds a dynamic and interactive element to the game, allowing players to challenge their friends and showcase their skills in a fast-paced, explosive showdown.
The game incorporates animations for the player character, providing a visual representation of movement and actions. The player can choose from different maps, either using default implementations or by loading custom maps from external files.

## Install dependencies
```pip3 install pygame```, ``` pip3 install pygame-menu```


## Run a game
Position yourself in the main directory. After that, execute following commands:

```cd ..``` ```python3 -m bomberman_2d.src.menu ```

## Run tests
From the parent directory run:

```python3 -m unittest tests/map_generation_test.py ```

```python3 -m unittest tests/bomb_test.py ```

```python3 -m unittest tests/explosion_test.py ```

If it's not working, try to run ```sudo python3 setup.py install ``` in the main directory and repeat the process.

## Controls 

### Single-Player
Arrow kyes for moving and space for planting the bomb
### Multi-Player
Arrow keys and space for player2, "wasd" and "e" for player1

## Selecting a custom map

Go to <b> Start --> Options --> Mapfile </b>. Here write just the name of the file without relative path or extension. For example: ```no_walls``` or ```all_walls```