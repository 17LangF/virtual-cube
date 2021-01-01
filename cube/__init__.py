'''
Virtual Cube Program - Made by Fred Lang.
Initiate Cube class.
'''

#Cube
class Cube:
    #Import methods
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

    class MoveError(Exception):
        """Raise when move is invalid."""

    #Assign attributes
    def __init__(self, size=3):
        self.cube = [[[i]*size for _ in range(size)] for i in 'ULFRBD']

        #Attributes
        self.size = size
        self.moves = []
        self.smoves = []
        self.showstyle = {
            'SHOW': True,
            'DIMENSION': 3,
            '3D': [38, 28, 0.1, 180, 9],
            '2D': ['██', 'fg,colour', True]
        }
        self.colours = {
            'U': (255,255,255),
            'L': (255,165,0),
            'F': (0,128,0),
            'R': (255,0,0),
            'B': (0,0,255),
            'D': (255,255,0)
        }
