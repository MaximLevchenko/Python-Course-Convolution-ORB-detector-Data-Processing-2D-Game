class Bomb:
    frame = 0

    def __init__(self, r, x, y, game_map, bomber):
        """
        Initialize a bomb with range 'r' at position (x, y) in the game.

        Args:
            r (int): The range of the bomb.
            x (int): The x-coordinate of the bomb's position.
            y (int): The y-coordinate of the bomb's position.
            game_map (List[List[int]]): The game map.
            bomber: The player who planted the bomb.
        """
        self.range = r
        self.pos_x = x
        self.pos_y = y
        self.time = 3000
        self.bomber = bomber
        self.sectors = []
        self.get_range(game_map)

    def update(self, dt):
        """
        Update the bomb over time, adjusting the frame and time.

        Args:
            dt (int): The time elapsed since the last update in milliseconds.
        """
        self.time = self.time - dt

        if self.time < 1000:
            self.frame = 2
        elif self.time < 2000:
            self.frame = 1

    def get_range(self, game_map):
        """
        Calculate and populate the bomb's explosion sectors based on the game map.

        Args:
            game_map (List[List[int]]): The game map.
        """
        self.sectors.append([self.pos_x, self.pos_y])

        for x in range(1, self.range):
            if game_map[self.pos_x + x][self.pos_y] == 1:
                break
            elif game_map[self.pos_x + x][self.pos_y] == 0 or game_map[self.pos_x - x][self.pos_y] == 3:
                self.sectors.append([self.pos_x + x, self.pos_y])
            elif game_map[self.pos_x + x][self.pos_y] == 2:
                self.sectors.append([self.pos_x + x, self.pos_y])
                break
        for x in range(1, self.range):
            if game_map[self.pos_x - x][self.pos_y] == 1:
                break
            elif game_map[self.pos_x - x][self.pos_y] == 0 or game_map[self.pos_x - x][self.pos_y] == 3:
                self.sectors.append([self.pos_x - x, self.pos_y])
            elif game_map[self.pos_x - x][self.pos_y] == 2:
                self.sectors.append([self.pos_x - x, self.pos_y])
                break
        for x in range(1, self.range):
            if game_map[self.pos_x][self.pos_y + x] == 1:
                break
            elif game_map[self.pos_x][self.pos_y + x] == 0 or game_map[self.pos_x][self.pos_y + x] == 3:
                self.sectors.append([self.pos_x, self.pos_y + x])
            elif game_map[self.pos_x][self.pos_y + x] == 2:
                self.sectors.append([self.pos_x, self.pos_y + x])
                break
        for x in range(1, self.range):
            if game_map[self.pos_x][self.pos_y - x] == 1:
                break
            elif game_map[self.pos_x][self.pos_y - x] == 0 or game_map[self.pos_x][self.pos_y - x] == 3:
                self.sectors.append([self.pos_x, self.pos_y - x])
            elif game_map[self.pos_x][self.pos_y - x] == 2:
                self.sectors.append([self.pos_x, self.pos_y - x])
                break
