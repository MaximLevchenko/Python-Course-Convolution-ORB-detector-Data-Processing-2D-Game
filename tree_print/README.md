# Tree Rendering in UTF16-Art


## Objective

The goal is to render a tree defined by a list of values in "UTF16-art". Each internal node of the tree contains two items: the node's name and a list of children (not necessarily in this order). The name can be any object except a list.

### Examples of Valid Trees
- Trivial tree with 1 node: `[1, []]`
- Trivial tree with 1 node with reversed order of ID and children: `[[], 2]`
- Trivial tree with 3 nodes: `[1, [2, 3]]`  
  (Leaf nodes in a tree with a height ≥ 2 can be written without an empty list of children for simplicity)

### Examples of Invalid Trees
- `None`
- `[]`
- `[666]`
- `[1, 2]`
- `(1, [2, 3])`

## Tree Rendering Rules
- The tree is rendered from top to bottom, left to right.
- A node is represented by its name, which is a string serialization of the object specified in the node definition.
- A node at depth N is indented N×{indent} characters from the left, where {indent} is always a positive integer > 1.
- If a node has K children, arrows are drawn as follows:
  - To the 1st to (K-1)th children: an arrow starting with `├` (UTF16: 0x251C)
  - To the Kth child: an arrow starting with `└` (UTF16: 0x2514)
- The arrow to a child node always ends with `>` (UTF16: 0x003E; standard "greater than").
- The total length of the arrow (including the initial character and `>`) is always {indent}, with the fill character being repeated `─` (UTF16: 0x2500).
- All children of a node are connected at the level of the start of the arrows with a vertical line `│` (UTF16: 0x2502); where there isn't a `├` or `└` as the initial character.
- If a node name contains the `\n` character, do not additionally indent the rest of the name after this character.
- Each line ends with the `\n` character.

## Additional Requirements
- For invalid input, the implementation must raise the exception `raise Exception('Invalid tree')`.
- The code style must adhere to PEP8 (you can ignore the line length requirement - C0301 and use single-letter variables in justified cases - C0103)
  - Test with `pylint --disable=C0301,C0103 trees.py`
- Use only built-in methods, i.e., no importing additional modules.

## Examples of Input and Output

### Example 1
**INPUT:**
```python
[[[1, [True, ['abc', 'def']]], [2, [3.14159, 6.023e23]]], 42]
```
**PARAMS:**
- **indent** = 4
- **separator** = '.'

**OUTPUT:**
```bash
42
├──>1
│...└──>True
│.......├──>abc
│.......└──>def
└──>2
....├──>3.14159
....└──>6.023e+23
```

### Example 2
**INPUT:**
```python
[[[1, [[True, ['abc', 'def']], [False, [1, 2]]]], [2, [3.14159, 6.023e23, 2.718281828]], [3, ['x', 'y']], [4, []]], 42]
```
**PARAMS:**
- **indent** = 4
- **separator** = '.'

**OUTPUT:**
```bash
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
```

### Example 3
**INPUT:**
```python
[6, [[[[1, [2, 3]], [42, [-43, 44]]], 4], 5]]
```
**PARAMS:**
- **indent** = 2
- **separator** = ' '

**OUTPUT:**
```bash
6
└>5
  └>4
    ├>1
    │ ├>2
    │ └>3
    └>42
      ├>-43
      └>44
```

### Example 4
**INPUT:**
```python
[6, [5, ['two\nlines']]]
```
**PARAMS:**
- **indent** = 2
- **separator** = ' '

**OUTPUT:**
```bash
6
└>5
  └>two
lines
```

## Required UTF16-Art Characters

- └ (UTF16: 0x2514)
- ├ (UTF16: 0x251C)
- ─ (UTF16: 0x2500)
- │ (UTF16: 0x2502)

## Sources

https://en.wikipedia.org/wiki/Box_Drawing









