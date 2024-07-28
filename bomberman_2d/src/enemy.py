import pygame
import random
from bomberman_2d.src.bomb import Bomb
from bomberman_2d.src.node import Node
from bomberman_2d.src.enums.algorithm import Algorithm


class Enemy:
    # Possible movement directions: [down, right, up, left]
    dire = [[1, 0, 1], [0, 1, 0], [-1, 0, 3], [0, -1, 2]]

    TILE_SIZE = 4

    def __init__(self, x, y, alg):
        """Initialize an enemy with specified position (x, y) and movement algorithm.

        Args:
            x (int): The initial x-coordinate of the enemy.
            y (int): The initial y-coordinate of the enemy.
            alg (Algorithm): The movement algorithm for the enemy (DFS or Dijkstra).
        """
        self.life = True
        self.path = []
        self.movement_path = []
        self.pos_x = x * Enemy.TILE_SIZE
        self.pos_y = y * Enemy.TILE_SIZE
        self.direction = 0
        self.frame = 0
        self.animation = []
        self.range = 3
        self.bomb_limit = 1
        self.plant = False
        self.algorithm = alg

    def move(self, map, bombs, explosions, enemy):
        """Move the enemy based on its current direction.

        Args:
            map (List[List[int]]): The game map.
            bombs (List[Bomb]): List of bomb objects.
            explosions (List[Explosion]): List of explosion objects.
            enemy (List[Enemy]): List of enemy objects.
        """
        if self.direction == 0:
            self.pos_y += 1
        elif self.direction == 1:
            self.pos_x += 1
        elif self.direction == 2:
            self.pos_y -= 1
        elif self.direction == 3:
            self.pos_x -= 1

        # Check if the enemy has reached the center of the next tile
        if self.pos_x % Enemy.TILE_SIZE == 0 and self.pos_y % Enemy.TILE_SIZE == 0:
            self.movement_path.pop(0)
            self.path.pop(0)
            if len(self.path) > 1:
                grid = self.create_grid(map, bombs, explosions, enemy)
                next = self.path[1]
                if grid[next[0]][next[1]] > 1:
                    self.movement_path.clear()
                    self.path.clear()

        # Animate the enemy movement
        if self.frame == 2:
            self.frame = 0
        else:
            self.frame += 1

    def make_move(self, map, bombs, explosions, enemy):
        """Make a move for the enemy.

        Args:
            map (List[List[int]]): The game map.
            bombs (List[Bomb]): List of bomb objects.
            explosions (List[Explosion]): List of explosion objects.
            enemy (List[Enemy]): List of enemy objects.
        """
        if not self.life:
            return
        if len(self.movement_path) == 0:
            if self.plant:
                bombs.append(self.plant_bomb(map))
                self.plant = False
                map[int(self.pos_x / Enemy.TILE_SIZE)][int(self.pos_y / Enemy.TILE_SIZE)] = 3
            if self.algorithm is Algorithm.DFS:
                self.dfs(self.create_grid(map, bombs, explosions, enemy))
            else:
                self.dijkstra(self.create_grid_dijkstra(map, bombs, explosions, enemy))

        else:
            self.direction = self.movement_path[0]
            self.move(map, bombs, explosions, enemy)

    def plant_bomb(self, map):
        """Plant a bomb at the current position of the enemy.

        Args:
            map (List[List[int]]): The game map.

        Returns:
            Bomb: The bomb object planted by the enemy.
        """
        b = Bomb(self.range, round(self.pos_x / Enemy.TILE_SIZE), round(self.pos_y / Enemy.TILE_SIZE), map, self)
        self.bomb_limit -= 1
        return b

    def check_death(self, exp):
        """Check if the enemy is hit by an explosion.

        Args:
            exp (List[Explosion]): List of explosion objects.
        """
        for e in exp:
            for s in e.sectors:
                if int(self.pos_x / Enemy.TILE_SIZE) == s[0] and int(self.pos_y / Enemy.TILE_SIZE) == s[1]:
                    self.life = False
                    return

    def dfs(self, grid):
        """
        Perform Depth-First Search to find a path for the enemy.

        Args:
            grid (List[List[int]]): The grid representing the game map.

        Returns:
            None: The path is stored in the instance variable `path`.
        """

        new_path = [[int(self.pos_x / Enemy.TILE_SIZE), int(self.pos_y / Enemy.TILE_SIZE)]]
        depth = 0
        if self.bomb_limit == 0:
            self.dfs_rec(grid, 0, new_path, depth)
        else:
            self.dfs_rec(grid, 2, new_path, depth)

        self.path = new_path

    def dfs_rec(self, grid, end, path, depth):
        """
        Recursive function for Depth-First Search.

        Args:
            grid (List[List[int]]): The grid representing the game map.
            end (int): The goal state for the search.
            path (List[List[int]]): The current path being explored.
            depth (int): The current depth of the search.

        Returns:
            None: The path is modified in-place.
        """
        last = path[-1]
        if depth > 200:
            return
        if grid[last[0]][last[1]] == 0 and end == 0:
            return
        elif end == 2:
            if grid[last[0] + 1][last[1]] == end or grid[last[0] - 1][last[1]] == end \
                    or grid[last[0]][last[1] + 1] == end \
                    or grid[last[0]][last[1] - 1] == end:
                if len(path) == 1 and end == 2:
                    self.plant = True
                return

        grid[last[0]][last[1]] = 9

        random.shuffle(self.dire)

        # safe
        if grid[last[0] + self.dire[0][0]][last[1] + self.dire[0][1]] == 0:
            path.append([last[0] + self.dire[0][0], last[1] + self.dire[0][1]])
            self.movement_path.append(self.dire[0][2])
        elif grid[last[0] + self.dire[1][0]][last[1] + self.dire[1][1]] == 0:
            path.append([last[0] + self.dire[1][0], last[1] + self.dire[1][1]])
            self.movement_path.append(self.dire[1][2])
        elif grid[last[0] + self.dire[2][0]][last[1] + self.dire[2][1]] == 0:
            path.append([last[0] + self.dire[2][0], last[1] + self.dire[2][1]])
            self.movement_path.append(self.dire[2][2])
        elif grid[last[0] + self.dire[3][0]][last[1] + self.dire[3][1]] == 0:
            path.append([last[0] + self.dire[3][0], last[1] + self.dire[3][1]])
            self.movement_path.append(self.dire[3][2])

        # unsafe
        elif grid[last[0] + self.dire[0][0]][last[1] + self.dire[0][1]] == 1:
            path.append([last[0] + self.dire[0][0], last[1] + self.dire[0][1]])
            self.movement_path.append(self.dire[0][2])
        elif grid[last[0] + self.dire[1][0]][last[1] + self.dire[1][1]] == 1:
            path.append([last[0] + self.dire[1][0], last[1] + self.dire[1][1]])
            self.movement_path.append(self.dire[1][2])
        elif grid[last[0] + self.dire[2][0]][last[1] + self.dire[2][1]] == 1:
            path.append([last[0] + self.dire[2][0], last[1] + self.dire[2][1]])
            self.movement_path.append(self.dire[2][2])
        elif grid[last[0] + self.dire[3][0]][last[1] + self.dire[3][1]] == 1:
            path.append([last[0] + self.dire[3][0], last[1] + self.dire[3][1]])
            self.movement_path.append(self.dire[3][2])
        else:
            if len(self.movement_path) > 0:
                path.pop(0)
                self.movement_path.pop(0)
        depth += 1
        self.dfs_rec(grid, end, path, depth)

    def dijkstra(self, grid):
        """
        Perform Dijkstra's algorithm to find the shortest path for the enemy.

        Args:
            grid (List[List[Node]]): The grid of Node objects representing the game map.

        Returns:
            None: The path is stored in the instance variable `path`.
        """
        # Set the goal for Dijkstra's algorithm based on bomb limit
        end = 1
        if self.bomb_limit == 0:
            end = 0

        # Initialize lists to track visited and open nodes, and set the current node
        visited = []
        open_list = []
        current = grid[int(self.pos_x / Enemy.TILE_SIZE)][int(self.pos_y / Enemy.TILE_SIZE)]
        current.weight = current.base_weight
        new_path = []

        # Main loop for Dijkstra's algorithm
        while True:
            # Mark the current node as visited
            visited.append(current)
            # Shuffle the movement directions to explore different paths
            random.shuffle(self.dire)

            # Check if the current node is the goal or the enemy is near a bomb
            if (current.value == end and end == 0) or \
                    (end == 1 and (
                            grid[current.x + 1][current.y].value == 1 or grid[current.x - 1][current.y].value == 1 or
                            grid[current.x][current.y + 1].value == 1 or grid[current.x][current.y - 1].value == 1)):
                # Reconstruct the path by backtracking from the goal node
                new_path.append([current.x, current.y])
                while True:
                    if current.parent is None:
                        break
                    current = current.parent
                    new_path.append([current.x, current.y])
                new_path.reverse()
                # print(new_path)
                # Convert the path to movement directions (0-3) and update enemy's path and movement_path
                for xd in range(len(new_path)):
                    if new_path[xd] is not new_path[-1]:
                        if new_path[xd][0] - new_path[xd + 1][0] == -1:
                            self.movement_path.append(1)  # Down
                        elif new_path[xd][0] - new_path[xd + 1][0] == 1:
                            self.movement_path.append(3)  # Up
                        elif new_path[xd][1] - new_path[xd + 1][1] == -1:
                            self.movement_path.append(0)  # Right
                        elif new_path[xd][1] - new_path[xd + 1][1] == 1:
                            self.movement_path.append(2)  # Left

                # If the goal is reached and it is to plant a bomb, set the plant flag
                if len(new_path) == 1 and end == 1:
                    self.plant = True
                self.path = new_path
                return

            # Explore neighbors of the current node
            for i in range(len(self.dire)):
                if current.x + self.dire[i][0] < len(grid) and current.y + self.dire[i][1] < len(grid):
                    neighbor = grid[current.x + self.dire[i][0]][current.y + self.dire[i][1]]
                    if neighbor.reach and neighbor not in visited:
                        if neighbor in open_list:
                            # Update the node in open_list if a shorter path is found
                            if neighbor.weight > current.weight + neighbor.base_weight:
                                neighbor.parent = current
                                neighbor.weight = current.weight + neighbor.base_weight
                                neighbor.direction = self.dire[i][2]
                        else:
                            # Add the neighbor to open_list if it's not there
                            neighbor.parent = current
                            neighbor.weight = current.weight + neighbor.base_weight
                            neighbor.direction = self.dire[i][2]
                            open_list.append(neighbor)

            # If there are no more open nodes, set a default path to the current position
            if len(open_list) == 0:
                self.path = [[int(self.pos_x / Enemy.TILE_SIZE), int(self.pos_y / Enemy.TILE_SIZE)]]
                return

            # Select the next node to explore based on the lowest weight in open_list
            next_node = open_list[0]
            for n in open_list:
                if n.weight < next_node.weight:
                    next_node = n
            open_list.remove(next_node)
            current = next_node

    def create_grid(self, map, bombs, explosions, enemys):
        """
    Create a grid for pathfinding algorithms.

    Args:
        map (List[List[int]]): The game map.
        bombs (List[Bomb]): List of bomb objects.
        explosions (List[Explosion]): List of explosion objects.
        enemys (List[Enemy]): List of enemy objects.

    Returns:
        List[List[int]]: A 2D grid representing the game map with additional information for pathfinding.
        """
        grid = [[0] * len(map) for r in range(len(map))]

        # 0 - safe
        # 1 - unsafe
        # 2 - destryable
        # 3 - unreachable

        for b in bombs:
            b.get_range(map)
            for x in b.sectors:
                grid[x[0]][x[1]] = 1
            grid[b.pos_x][b.pos_y] = 3

        for e in explosions:
            for s in e.sectors:
                grid[s[0]][s[1]] = 3

        for i in range(len(map)):
            for j in range(len(map[i])):
                if map[i][j] == 1:
                    grid[i][j] = 3
                elif map[i][j] == 2:
                    grid[i][j] = 2

        for x in enemys:
            if x == self:
                continue
            elif not x.life:
                continue
            else:
                grid[int(x.pos_x / Enemy.TILE_SIZE)][int(x.pos_y / Enemy.TILE_SIZE)] = 2

        return grid

    def create_grid_dijkstra(self, map, bombs, explosions, enemys):
        """
           Create a grid of Node objects for Dijkstra's algorithm.

           Args:
               map (List[List[int]]): The game map.
               bombs (List[Bomb]): List of bomb objects.
               explosions (List[Explosion]): List of explosion objects.
               enemys (List[Enemy]): List of enemy objects.

           Returns:
               List[List[Node]]: A 2D grid of Node objects representing the game map with additional information for Dijkstra's algorithm.
        """
        grid = [[None] * len(map) for r in range(len(map))]


        # 0 - safe
        # 1 - destroyable
        # 2 - unreachable
        # 3 - unsafe
        for i in range(len(map)):
            for j in range(len(map)):
                if map[i][j] == 0:
                    grid[i][j] = Node(i, j, True, 1, 0)
                elif map[i][j] == 2:
                    grid[i][j] = Node(i, j, False, 999, 1)
                elif map[i][j] == 1:
                    grid[i][j] = Node(i, j, False, 999, 2)
                elif map[i][j] == 3:
                    grid[i][j] = Node(i, j, False, 999, 2)

        for b in bombs:
            b.get_range(map)
            for x in b.sectors:
                grid[x[0]][x[1]].weight = 5
                grid[x[0]][x[1]].value = 3
            grid[b.pos_x][b.pos_y].reach = False

        for e in explosions:
            for s in e.sectors:
                grid[s[0]][s[1]].reach = False  # to delete from pathfinding algs

        for x in enemys:
            if x == self:
                continue
            elif not x.life:
                continue
            else:
                # so it will mark other player's positions as destroyable in order to favour the bomb placement here
                grid[int(x.pos_x / Enemy.TILE_SIZE)][int(x.pos_y / Enemy.TILE_SIZE)].reach = False
                grid[int(x.pos_x / Enemy.TILE_SIZE)][int(x.pos_y / Enemy.TILE_SIZE)].value = 1
        return grid

    def load_animations(self, en, scale):
        """
        Load enemy animations based on the character and scale.

        Args:
            en (str): The character identifier for enemy animations.
            scale (int): The scale factor for resizing the loaded images.

        Returns:
            None: The loaded animations are stored in the `animation` attribute.

        Note:
            The `en` parameter is an empty string for hero animations and a character identifier for enemy animations.
            The loaded animations are organized into lists for front, right, back, and left directions.
        """
        front = []
        back = []
        left = []
        right = []
        resize_width = scale
        resize_height = scale

        image_path = '../images/enemy/e'
        if en == '':
            image_path = '../images/hero/p'

        f1 = pygame.image.load(image_path + en + 'f0.png')
        f2 = pygame.image.load(image_path + en + 'f1.png')
        f3 = pygame.image.load(image_path + en + 'f2.png')

        f1 = pygame.transform.scale(f1, (resize_width, resize_height))
        f2 = pygame.transform.scale(f2, (resize_width, resize_height))
        f3 = pygame.transform.scale(f3, (resize_width, resize_height))

        front.append(f1)
        front.append(f2)
        front.append(f3)

        r1 = pygame.image.load(image_path + en + 'r0.png')
        r2 = pygame.image.load(image_path + en + 'r1.png')
        r3 = pygame.image.load(image_path + en + 'r2.png')

        r1 = pygame.transform.scale(r1, (resize_width, resize_height))
        r2 = pygame.transform.scale(r2, (resize_width, resize_height))
        r3 = pygame.transform.scale(r3, (resize_width, resize_height))

        right.append(r1)
        right.append(r2)
        right.append(r3)

        b1 = pygame.image.load(image_path + en + 'b0.png')
        b2 = pygame.image.load(image_path + en + 'b1.png')
        b3 = pygame.image.load(image_path + en + 'b2.png')

        b1 = pygame.transform.scale(b1, (resize_width, resize_height))
        b2 = pygame.transform.scale(b2, (resize_width, resize_height))
        b3 = pygame.transform.scale(b3, (resize_width, resize_height))

        back.append(b1)
        back.append(b2)
        back.append(b3)

        l1 = pygame.image.load(image_path + en + 'l0.png')
        l2 = pygame.image.load(image_path + en + 'l1.png')
        l3 = pygame.image.load(image_path + en + 'l2.png')

        l1 = pygame.transform.scale(l1, (resize_width, resize_height))
        l2 = pygame.transform.scale(l2, (resize_width, resize_height))
        l3 = pygame.transform.scale(l3, (resize_width, resize_height))

        left.append(l1)
        left.append(l2)
        left.append(l3)

        self.animation.append(front)
        self.animation.append(right)
        self.animation.append(back)
        self.animation.append(left)

