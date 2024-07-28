
"""Module containing the Explosion class."""
from bomberman_2d.src.enums.power_up_type import PowerUpType
from bomberman_2d.src.power_up import PowerUp


class Explosion:
    """Class representing an explosion in the game."""
    bomber = None

    def __init__(self, x, y, r):
        """Initialize an explosion with a source position (x, y) and range (r).

        Args:
            x (int): The x-coordinate of the source position.
            y (int): The y-coordinate of the source position.
            r (int): The range of the explosion.
        """

        self.source_x = x
        self.source_y = y
        self.range = r
        self.time = 300
        self.frame = 0
        self.sectors = []

    def explode(self, game_map, bombs, b, power_ups):
        """Trigger the explosion, removing the bomb and initiating the bomb chain.

        Args:
            game_map (List[List[int]]): The game map representing the grid.
            bombs (List[Bomb]): The list of bombs in the game.
            b (Bomb): The bomb to be exploded.
            power_ups (List[PowerUp]): The list of power-ups in the game.
        """
        self.bomber = b.bomber
        self.sectors.extend(b.sectors)
        bombs.remove(b)
        self.bomb_chain(bombs, game_map, power_ups)

    def bomb_chain(self, bombs, game_map, power_ups):
        """Initiate a chain reaction, triggering explosions for bombs in the sectors.

        Args:
            bombs (List[Bomb]): The list of bombs in the game.
            game_map (List[List[int]]): The game map representing the grid.
            power_ups (List[PowerUp]): The list of power-ups in the game.
        """

        for s in self.sectors:
            for x in power_ups:
                if x.pos_x == s[0] and x.pos_y == s[1]:
                    power_ups.remove(x)

            for x in bombs:
                if x.pos_x == s[0] and x.pos_y == s[1]:
                    game_map[x.pos_x][x.pos_y] = 0
                    x.bomber.bomb_limit += 1
                    self.explode(game_map, bombs, x, power_ups)

    def clear_sectors(self, game_map, random, power_ups):
        """Clear the sectors, adding power-ups and updating the game_map.

        Args:
            game_map (List[List[int]]): The game map representing the grid.
            random: The random module for generating random numbers.
            power_ups (List[PowerUp]): The list of power-ups in the game.
        """
        for i in self.sectors:
            if game_map[i[0]][i[1]] == 2:
                r = random.randint(0, 9)
                if r == 0:
                    power_ups.append(PowerUp(i[0], i[1], PowerUpType.BOMB))
                elif r == 1:
                    power_ups.append(PowerUp(i[0], i[1], PowerUpType.FIRE))

            game_map[i[0]][i[1]] = 0

    def update(self, dt):
        """Update the explosion over time, adjusting the frame and time.

        Args:
            dt (int): The time elapsed since the last update.
        """
        self.time = self.time - dt

        if self.time < 100:
            self.frame = 2
        elif self.time < 200:
            self.frame = 1
