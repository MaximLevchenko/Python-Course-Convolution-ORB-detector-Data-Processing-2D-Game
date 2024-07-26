#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Version 0.1

Cílem je vykreslit v "UTF16-artu" strom definovaný listem hodnot. Každý vnitřní uzel stromu obsahuje vždy dvě položky: název uzlu a seznam potomků (nemusí být nutně v tomto pořadí). Názvem může být jakýkoli objekt kromě typu list (seznam).

Příklady validních stromů:
    - triviální strom o 1 uzlu: [1, []]
    - triviální strom o 1 uzlu s opačným pořadím ID a potomků: [[], 2]
    - triviální strom o 3 uzlech: [1, [2, 3]]
        (listové uzly ve stromu o výšce >= 2 mohou být pro zjednodušení zapsány i bez prázdného seznamu potomků)

Příklady nevalidních stromů:
    - None
    - []
    - [666]
    - [1, 2]
    - (1, [2, 3])


Strom bude vykreslen podle následujících pravidel:
    - Vykresluje se shora dolů, zleva doprava.
    - Uzel je reprezentován jménem, které je stringovou serializací objektu daného v definici uzlu.
    - Uzel v hloubce N bude odsazen zlava o N×{indent} znaků, přičemž hodnota {indent} bude vždy kladné celé číslo > 1.
    - Má-li uzel K potomků, povede:
        - k 1. až K-1. uzlu šipka začínající znakem ├ (UTF16: 0x251C)
        - ke K. uzlu šipka začínající znakem └ (UTF16: 0x2514)
    - Šipka k potomku uzlu je vždy zakončena znakem > (UTF16: 0x003E; klasické "větší než").
    - Celková délka šipky (včetně úvodního znaku a koncového ">") je vždy {indent}, výplňovým znakem je zopakovaný znak ─ (UTF16: 0x2500).
    - Všichni potomci uzlu jsou spojeni na úrovni počátku šipek svislou čarou │ (UTF16: 0x2502); tedy tam, kde není jako úvodní znak ├ nebo └.
    - Pokud název uzlu obsahuje znak `\n` neodsazujte nijak zbytek názvu po tomto znaku.
    - Každý řádek je ukončen znakem `\n`.

Další požadavky na vypracovní:
    - Pro nevalidní vstup musí implementace vyhodit výjimku `raise Exception('Invalid tree')`.
    - Mít codestyle v souladu s PEP8 (můžete ignorovat požadavek na délku řádků - C0301 a používat v odůvodněných případech i jednopísmenné proměnné - C0103)
        - otestujte si pomocí `pylint --disable=C0301,C0103 trees.py`
    - Vystačit si s buildins metodami, tj. žádné importy dalších modulů.


Příklady vstupu a výstupu:
INPUT:
[[[1, [True, ['abc', 'def']]], [2, [3.14159, 6.023e23]]], 42]

PARAMS:
    indent = 4
    separator = '.'

OUTPUT:
42
├──>1
│...└──>True
│.......├──>abc
│.......└──>def
└──>2
....├──>3.14159
....└──>6.023e+23

INPUT:
[[[1, [[True, ['abc', 'def']], [False, [1, 2]]]], [2, [3.14159, 6.023e23, 2.718281828]], [3, ['x', 'y']], [4, []]], 42]

PARAMS:
    indent = 4
    separator = '.'

OUTPUT:
42
├──>1
│...├──>True
│...│...├──>abc
│...│...└──>def
│...└──>False
│.......├──>1
│.......└──>2
├──>2
│...├──>3.14159
│...├──>6.023e+23
│...└──>2.718281828
├──>3
│...├──>x
│...├──>y
└──>4


INPUT:
[6, [[[[1, [2, 3]], [42, [-43, 44]]], 4], 5]]

PARAMS:
    indent = 2
    separator = ' '

OUTPUT:
6
└>5
  └>4
    ├>1
    │ ├>2
    │ └>3
    └>42
      ├>-43
      └>44

INPUT:
[6, [5, ['dva\nradky']]]

PARAMS:
    indent = 2
    separator = ' '

OUTPUT:
6
└>5
  └>dva
radky

Potřebné UTF16-art znaky:
└ ├ ─ │

Odkazy:
https://en.wikipedia.org/wiki/Box_Drawing
"""


def print_structure_info(tree, indent, separator: str):
    """
    Generate a visual representation of a tree structure using custom indentation and separator characters.

    Args:
        tree (list): A list representing the parsed tree structure.
        indent (int): The number of spaces for indentation.
        separator (str): The character used for separating tree elements.

    Returns:
        str: A string containing the visual representation of the tree.
    """
    result = ""  # Initialize an empty string to accumulate the output

    # if last element level is lower than the first one, then the list should be reversed
    if tree[-1].get("level") < tree[0].get("level"):  # means that it should be reversed
        tree = reversed(tree)

    for item in tree:
        output = ""
        if item['type'] == 'not list':  # we are at base case dictionaries
            if item.get("is_last"):
                output += ((item.get("level") - 1) * separator * indent +
                           ("└" + (indent - 2) * "─" + ">" if item.get("level") > 0 else '') + f"{item.get('value')}")
            else:
                output += ((item.get("level") - 1) * separator * indent +
                           ("├" + (indent - 2) * "─" + ">" if item.get("level") > 0 else '') + f"{item.get('value')}")
            for print_level in item.get("levels_to_print"):
                if output[print_level * indent] != "├" and output[print_level * indent] != "└":
                    output = output[:print_level * indent] + '│' + output[print_level * indent + 1:]
            result += output + '\n'  # Concatenate the output and add a newline

        else:  # we go into recursion
            result += print_structure_info(item.get("contents", []), indent, separator)  # Recursively accumulate output

    return result  # Return the accumulated output as a string


def no_lists_in_structure(structure):
    """
    Check if there are no lists within the provided structure.

    Args:
        structure (list): A list to be checked for the absence of nested lists.

    Returns:
        bool: True if there are no nested lists, False otherwise.
    """
    for item in structure:
        if isinstance(item, list):
            return False
    return True


def at_least_one_non_list_in_structure(structure):
    """
    Check if there is at least one non-list element within the provided structure.

    Args:
        structure (list): A list to be checked for the presence of at least one non-list element.

    Returns:
        bool: True if at least one non-list element is found, False otherwise.
    """
    for item in structure:
        if not isinstance(item, list):
            return True
    return False


def custom_sort_key(item):
    """
    Custom sorting key function to differentiate between lists and non-list elements during sorting.

    Args:
        item: An element to be sorted.

    Returns:
        int: 0 for non-list elements, 1 for lists.
    """
    return 0 if not isinstance(item, list) else 1


def parse_structure(structure, level=0, is_last=False, should_set_is_last=False, levels_before_to_show=None):
    """
    Recursively parse a nested tree structure to prepare it for rendering.

    Args:
        structure: The nested tree structure to be parsed.
        level (int): The current level of the tree.
        is_last (bool): Indicates if the current item is the last at its level.
        should_set_is_last (bool): Flag for setting the last item in a group.
        levels_before_to_show (list): A list of levels before the current one for showing connectors.

    Returns:
        dict: A parsed representation of the input structure.
    """
    if levels_before_to_show is None:
        levels_before_to_show = []

    if isinstance(structure, list):
        contents = []
        structure.sort(key=custom_sort_key)

        for i, item in enumerate(structure):
            list_count_inside_item = 0

            if isinstance(item, list):
                list_count_inside_item = sum(1 for i_in_item in item if isinstance(i_in_item, list))

            new_level = level + 1 if at_least_one_non_list_in_structure(structure) and isinstance(item, list) else level

            if is_last and should_set_is_last:
                is_last = True
                should_set_is_last = False
            elif not at_least_one_non_list_in_structure(structure) or no_lists_in_structure(
                    structure) or list_count_inside_item == 1:
                is_last = i == len(structure) - 1 or is_last
                should_set_is_last = is_last
            else:
                is_last = False

            if at_least_one_non_list_in_structure(structure) and isinstance(item, list):
                levels_before_to_show.append(level)
                for content in contents:
                    if content.get("is_last"):
                        levels_before_to_show.remove(level - 1)

            result = parse_structure(item, new_level, is_last, should_set_is_last, levels_before_to_show.copy())
            is_last = False
            contents.append(result)

        contents = [c for c in contents if c is not None]  # Remove None values
        if contents:  # Check if there's at least one non-empty item
            result = {"type": "list", "level": level, "contents": contents}
        else:
            result = None  # Skip empty lists
        return result

    return {"type": "not list", "level": level, "value": structure, "is_last": is_last,
            "levels_to_print": levels_before_to_show}


# if (len == 0 and level == 0) or None  then its not okay
# if not (isinstance(list) or isinstance(int) or isinstance(float) or isinstance(str) or isinstance(bool)

def count_of_non_list_elements(structure):
    """
       Count the number of non-list elements in a list.

       This function counts the number of elements in a given list that are not themselves lists.

       Args:
           structure (list): The list in which non-list elements need to be counted.

       Returns:
           int: The number of non-list elements in the list.

       Example:
           You can use this function to count the number of non-list elements in a given list. For example, if you have
           a list 'my_list' containing various elements, you can call 'count_of_non_list_elements(my_list)' to get the
           count of non-list elements in 'my_list'.

       Note:
           Non-list elements can include integers, floats, booleans, and strings.
    """
    counter = 0
    for item in structure:
        if not isinstance(item, list):
            counter += 1
    return counter


def is_valid_tree(structure, level=0):
    """
        Check the validity of a nested tree structure.

        This function checks if a given tree structure is valid based on certain criteria. It performs a recursive
        validation of the structure and raises an exception if it is found to be invalid.

        Args:
            structure (list): The nested tree structure to be validated.
            level (int, optional): The current level of the tree during recursion. Defaults to 0.

        Returns:
            bool: True if the structure is valid, False if it is not.

        Raises:
            Exception: If the structure is found to be invalid.

        Example:
            To check the validity of a tree structure, you can call this function and provide the structure as the
            'structure' argument. If the structure is valid, the function returns True. If it is invalid, an Exception
            is raised with the message 'Invalid tree'.

        Note:
            A valid tree structure is one that adheres to the specified rules in the problem statement.
    """
    if structure is None:
        return False
    if level == 0:
        if (isinstance(structure, list) and len(structure) == 0 or
                isinstance(structure, list) and count_of_non_list_elements(structure) > 1):
            return False
    elif not isinstance(structure, (list, int, float, bool, str)):
        return False

    # if (isinstance(structure, list) and (len(structure) == 0 and level == 0) or structure is None or
    #         (isinstance(structure, list) and level == 0 and count_of_non_list_elements(structure) > 1)
    #         or not isinstance(structure, (list, int, float, bool, str))):
    #     raise Exception('Invalid tree')
    elif isinstance(structure, list):
        for node in structure:
            if not isinstance(structure, (list, int, float, bool, str)):
                return False
            new_level = level + 1 if at_least_one_non_list_in_structure(structure) and isinstance(node, list) else level
            return is_valid_tree(node, new_level)
    return True


def render_tree(tree: list = None, indent: int = 2, separator: str = '') -> str:
    """
    Render a tree structure and return its visual representation as a string.

    Args:
        tree (list): The nested tree structure to be rendered.
        indent (int): The number of spaces for indentation.
        separator (str): The character used for separating tree elements.

    Returns:
        str: A string containing the visual representation of the tree.
    """
    if not is_valid_tree(tree):
        raise Exception('Invalid tree')
    new_tree = parse_structure(tree)
    result = print_structure_info([new_tree], indent, separator)
    print(result)
    return result


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    nested_structure = [1,2,3,4,5]
    indent_main = 2
    separator_main = " "
    render_tree(nested_structure, indent_main, separator_main)
