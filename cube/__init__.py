"""Package to visualise and simulate a Rubik's Cube."""


class Cube:
    """
    A class which represents a Rubik's Cube.

    Attributes
    ----------
    cube : list of list of list of str
        3-dimentional list of size 6*N*N for an NxN cube which stores
        all stickers of the cube. Each sticker must be a character in
        'ULFRBD' and can be accessed by cube[s][y][x] where s is the
        face (0-5 representing the U, L, F, R, B, D faces respectively)
        and y, x are the row and column indexes of the sticker.
    size : int
        Number of cubies on each edge of the cube.
    moves : list of str
        List of moves applied to the cube after smoves.
    smoves : list of str
        List of moves applied as a scramble or as set-up moves.
    show_style : dict of {str: int or list}
        Stores the default or last used style for showing the cube.
    colours : dict of {str: tuple of int}
        Stores the RGB values for the colour of each of the 6 faces.

    Raises
    ------
    CubeError
        If there is a problem which stops a cube method.
    MoveError
        If a move cannot be interpreted or is invalid.
    """

    from ._colour import colour
    from ._input import input
    from ._invert import invert
    from ._link import link
    from ._mirror import mirror
    from ._move import move
    from ._movecount import movecount
    from ._play import play
    from ._repeat import repeat
    from ._reset import reset
    from ._scramble import scramble
    from ._show import show, show2D, show3D
    from ._simplify import simplify
    from ._solve import solve
    from ._speedsolve import speedsolve
    from ._undo import undo

    def __init__(self, size: int = 3):
        """
        Initialise Cube class with size of cube.

        Parameters
        ----------
        size : int, default=3
            Number of cubies on each edge of the cube.
        """
        self.cube = [[[i]*size for _ in range(size)] for i in 'ULFRBD']
        self.size = size
        self.moves = []
        self.smoves = []
        self.show_style = {
            'DIMENSION': 3,
            '3D': [38, 28, 0.1, 180, 9],
            '2D': ['\u2588\u2588', 'fg,colour', True]
        }
        self.colours = {
            'U': (255,255,255),
            'L': (255,165,0),
            'F': (0,128,0),
            'R': (255,0,0),
            'B': (0,0,255),
            'D': (255,255,0)
        }


class CubeError(Exception):
    """Raise when there is a problem which stops a cube method."""


class MoveError(Exception):
    """Raise when a move cannot be interpreted or is invalid."""
