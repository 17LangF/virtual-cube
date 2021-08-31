"""Save and load cube attributes to and from a file."""

import ast

from cube import Cube


def load(filename: str) -> Cube:
    """
    Load a cube from a previously saved file.

    Parameters
    ----------
    filename : str
        Name of previously saved file.

    Returns
    -------
    Cube
        Cube loaded from file.
    """
    with open(filename, encoding='utf-8') as file:
        data = file.read().splitlines()

    state, size, moves, smoves, show_style, colours = data
    cube = Cube()
    size = int(size)
    state = list(state)
    state = [state[y:y + size] for y in range(0, len(state), size)]
    state = [state[s:s + size] for s in range(0, 6 * size, size)]

    cube.cube = state
    cube.size = size
    cube.moves = moves.split()
    cube.smoves = smoves.split()
    cube.show_style = ast.literal_eval(show_style)
    cube.colours = ast.literal_eval(colours)
    return cube


def save(cube, filename: str):
    """
    Save cube attributes to a file.

    Parameters
    ----------
    filename : str
        Name of file to save to.
    """
    attributes = (
        ''.join(x for s in cube.cube for y in s for x in y),
        str(cube.size),
        ' '.join(cube.moves),
        ' '.join(cube.smoves),
        str(cube.show_style),
        str(cube.colours)
    )

    with open(filename, 'w', encoding='utf-8') as file:
        file.write('\n'.join(attributes))
