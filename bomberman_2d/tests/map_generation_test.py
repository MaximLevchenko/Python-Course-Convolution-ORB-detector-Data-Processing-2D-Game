import unittest
from bomberman_2d.src import game


class MyTestCase(unittest.TestCase):
    """
    Test case for map generation with a focus on corners.
    """

    """
    Test map generation with a focus on corners.

    Assert that specific grid positions in the corners have the expected values after map generation.
    """
    def test_map_generation_corners(self):
        grid = [row[:] for row in game.GRID_BASE]
        game.generate_map(grid)
        self.assertEqual(0, grid[1][1])
        self.assertEqual(0, grid[1][2])
        self.assertEqual(0, grid[2][1])

        l = len(grid)

        self.assertEqual(0, grid[l - 2][1])
        self.assertEqual(0, grid[l - 2][2])
        self.assertEqual(0, grid[l - 3][1])

        self.assertEqual(0, grid[1][l - 2])
        self.assertEqual(0, grid[1][l - 3])
        self.assertEqual(0, grid[2][l - 2])

        self.assertEqual(0, grid[l - 2][l - 2])
        self.assertEqual(0, grid[l - 2][l - 3])
        self.assertEqual(0, grid[l - 3][l - 2])


if __name__ == '__main__':
    unittest.main()

