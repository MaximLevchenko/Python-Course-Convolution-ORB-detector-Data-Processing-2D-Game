"""Module containing Node class"""

class Node:
    """
        A class representing a node in a search algorithm.

        Attributes:
            parent (Node): The parent node.
            weight (float): The weight of the node.
            direction (int): The direction of the node.
            x (int): The x-coordinate of the node.
            y (int): The y-coordinate of the node.
            reach (int): The reach value of the node.
            base_weight (float): The base weight of the node.
            value: The value of the node.

        Methods:
            __init__: Initializes a new instance of the Node class.

    """
    parent = None
    weight = None
    direction = 1

    def __init__(self, px, py, reach, base_weight, value):
        """
               Initializes a new instance of the Node class.

               Args:
                   px (int): The x-coordinate of the node.
                   py (int): The y-coordinate of the node.
                   reach (int): The reach value of the node.
                   base_weight (float): The base weight of the node.
                   value: The value of the node.

               Returns:
                   None

        """
        self.x = px
        self.y = py
        self.reach = reach
        self.base_weight = base_weight
        self.value = value
