"""Module containing the power up Class"""

class PowerUp:
    """
      A class representing a power-up in the game.

      Attributes:
          pos_x (int): The x-coordinate of the power-up.
          pos_y (int): The y-coordinate of the power-up.
          type: The type of the power-up.

      Methods:
          __init__: Initializes a new instance of the PowerUp class.

    """
    def __init__(self, x, y, power_type):
        """
                Initializes a new instance of the PowerUp class.

                Args:
                    x (int): The x-coordinate of the power-up.
                    y (int): The y-coordinate of the power-up.
                    power_type: The type of the power-up.

                Returns:
                    None

        """
        self.pos_x = x
        self.pos_y = y
        self.type = power_type
