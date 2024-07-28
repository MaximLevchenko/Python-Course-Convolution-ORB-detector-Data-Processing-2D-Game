"""Module containing the main menu loop"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pygame
import pygame_menu
import bomberman_2d.src.game
from bomberman_2d.src.enums.algorithm import Algorithm

COLOR_BACKGROUND = (0, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
FPS = 60.0
MENU_BACKGROUND_COLOR = (11, 218, 81)
MENU_TITLE_COLOR = (255, 0, 0)
WINDOW_SCALE = 0.75

pygame.display.init()
INFO = pygame.display.Info()
TILE_SIZE = int(INFO.current_h * 0.035)
WINDOW_SIZE = (13 * TILE_SIZE, 13 * TILE_SIZE)

clock = None
player_alg = Algorithm.PLAYER
en1_alg = Algorithm.DIJKSTRA
en2_alg = Algorithm.DFS
en3_alg = Algorithm.DIJKSTRA
multiplayer = True
map_file_path = None

selected_map_file = None
surface = pygame.display.set_mode(WINDOW_SIZE)


def read_map_from_file(file_path):
    """
        Read the map data from a file.

        Args:
            file_path (str): The path to the map file.

        Returns:
            List[List[int]]: The map data.
    """
    with open(file_path, 'r') as file:
        content = file.read()
        return eval(content)


def change_map_file(value):
    """
        Change the selected map file.

        Args:
            value (str): The selected map file.

        Returns:
            None
    """
    global selected_map_file
    selected_map_file = "../maps/" + value + ".txt"


def change_default_map(value, c):
    """
       Change the default map.

       Args:
           value: The value (not used).
           c: The choice (not used).

       Returns:
           None
    """
    global map_file_path
    map_file_path = None


def change_game_mode(value, c):
    """
        Change the game mode (multiplayer or single-player).

        Args:
            value: The value (not used).
            c: The choice representing the game mode.

        Returns:
            None
    """
    global multiplayer
    multiplayer = c


def change_player(value, c):
    """
       Change the player character.

       Args:
           value: The value (not used).
           c: The choice representing the player character.

       Returns:
           None
    """
    global player_alg
    player_alg = c


def change_enemy1(value, c):
    """
        Change the first enemy character.

        Args:
            value: The value (not used).
            c: The choice representing the first enemy character.

        Returns:
            None
    """
    global en1_alg
    en1_alg = c


def change_enemy2(value, c):
    """
       Change the second enemy character.

       Args:
           value: The value (not used).
           c: The choice representing the second enemy character.

       Returns:
           None
    """
    global en2_alg
    en2_alg = c


def change_enemy3(value, c):
    """
        Change the third enemy character.

        Args:
            value: The value (not used).
            c: The choice representing the third enemy character.

        Returns:
            None
    """
    global en3_alg
    en3_alg = c


def run_game():
    """
        Run the Bomberman game.

        Returns:
            None
    """
    if selected_map_file:
        # Read the map from the selected file
        custom_map = read_map_from_file(selected_map_file)
        bomberman_2d.src.game.game_init(surface, player_alg, en1_alg, en2_alg, en3_alg, multiplayer, TILE_SIZE, custom_map)
    else:
        # Use the default map
        bomberman_2d.src.game.game_init(surface, player_alg, en1_alg, en2_alg, en3_alg, multiplayer, TILE_SIZE)


def main_background():
    """
        Set the main menu background.

        Returns:
            None
    """
    global surface
    surface.fill(COLOR_BACKGROUND)


def menu_loop():
    """
       Main loop for the menu.

       Returns:
           None
    """
    pygame.init()

    pygame.display.set_caption('Bomberman')
    clock = pygame.time.Clock()

    menu_theme = pygame_menu.Theme(
        selection_color=COLOR_WHITE,
        widget_font=pygame_menu.font.FONT_BEBAS,
        title_font_size=TILE_SIZE,
        title_font_color=COLOR_BLACK,
        title_font=pygame_menu.font.FONT_BEBAS,
        widget_font_color=COLOR_BLACK,
        widget_font_size=int(TILE_SIZE * 0.7),
        background_color=MENU_BACKGROUND_COLOR,
        title_background_color=MENU_TITLE_COLOR,

    )

    play_menu = pygame_menu.Menu(
        theme=menu_theme,
        height=int(WINDOW_SIZE[1] * WINDOW_SCALE),
        width=int(WINDOW_SIZE[0] * WINDOW_SCALE),
        title='Play menu'
    )

    play_options = pygame_menu.Menu(
        theme=menu_theme,
        height=int(WINDOW_SIZE[1] * WINDOW_SCALE),
        width=int(WINDOW_SIZE[0] * WINDOW_SCALE),
        title='Options'
    )
    play_options.add.selector("Character 1", [("Player", Algorithm.PLAYER), ("DFS", Algorithm.DFS),
                                              ("DIJKSTRA", Algorithm.DIJKSTRA), ("None", Algorithm.NONE)],
                              onchange=change_player)
    play_options.add.selector("Character 2", [("DIJKSTRA", Algorithm.DIJKSTRA), ("DFS", Algorithm.DFS),
                                              ("None", Algorithm.NONE)], onchange=change_enemy1)
    play_options.add.selector("Character 3", [("DIJKSTRA", Algorithm.DIJKSTRA), ("DFS", Algorithm.DFS),
                                              ("None", Algorithm.NONE)], onchange=change_enemy2, default=1)
    play_options.add.selector("Character 4", [("DIJKSTRA", Algorithm.DIJKSTRA), ("DFS", Algorithm.DFS),
                                              ("None", Algorithm.NONE)], onchange=change_enemy3)
    play_options.add.selector("Multiplayer Mode", [("Yes", True), ("No", False)], onchange=change_game_mode)
    play_options.add.text_input('Map File: ', default='', onchange=change_map_file)
    play_options.add.button('Back', pygame_menu.events.BACK)
    play_menu.add.button('Start', run_game)

    play_menu.add.button('Options', play_options)
    play_menu.add.button('Return  to  main  menu', pygame_menu.events.BACK)

    about_menu_theme = pygame_menu.themes.Theme(
        selection_color=COLOR_WHITE,
        widget_font=pygame_menu.font.FONT_BEBAS,
        title_font_size=TILE_SIZE,
        title_font_color=COLOR_BLACK,
        title_font=pygame_menu.font.FONT_BEBAS,
        widget_font_color=COLOR_BLACK,
        widget_font_size=int(TILE_SIZE * 0.5),
        background_color=MENU_BACKGROUND_COLOR,
        title_background_color=MENU_TITLE_COLOR
    )

    main_menu = pygame_menu.Menu(
        theme=menu_theme,
        height=int(WINDOW_SIZE[1] * WINDOW_SCALE),
        width=int(WINDOW_SIZE[0] * WINDOW_SCALE),
        onclose=pygame_menu.events.EXIT,
        title='Main menu'
    )

    main_menu.add.button('Play', play_menu)
    main_menu.add.button('Quit', pygame_menu.events.EXIT)

    running = True
    while running:

        clock.tick(FPS)

        main_background()

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        if main_menu.is_enabled():
            main_menu.mainloop(surface, main_background)

        pygame.display.flip()

    exit()


if __name__ == "__main__":
    menu_loop()
