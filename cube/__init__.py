'''
Virtual Cube Program - Made by Fred Lang.
Initiate Cube class.
'''

#Cube
class Cube:
    #Import methods
    from ._commutator import commutator
    from ._conjugate import conjugate
    from ._input import input
    from ._invert import invert
    from ._link import link
    from ._move import move
    from ._movecount import movecount
    from ._orient import orient
    from ._play import play
    from ._repeat import repeat
    from ._reset import reset
    from ._reverse import reverse
    from ._scramble import scramble
    from ._show import show, show3D
    from ._simplify import simplify
    from ._solve import solve
    from ._speedsolve import speedsolve
    from ._undo import undo

    #Assign attributes
    def __init__(self, size=3):
        self.cube = [[[i]*size for x in range(size)] for i in 'ULFRBD']

        #Attributes
        self.size = size
        self.moves = []
        self.smoves = []
        self.showstyle = {
            'SHOW': True,
            'DIMENSION': 3,
            '3D INFO': [45, 28, 0.1, 200, 8],
            '3D COORDS': {2: []},
            'STICKER': '██',
            'COLOUR_CODES': 'fg,colour',
            'SPACES': True
        }
        self.colours = {
            'U': (255,255,255),
            'L': (255,165,0),
            'F': (0,128,0),
            'R': (255,0,0),
            'B': (0,0,255),
            'D': (255,255,0)
        }

        #Functions
        self.functions = {
            'RESET': self.reset,
            'SCRAMBLE': self.scramble,
            'MOVE': self.move,
            'SHOW': self.show,
            'EXIT': exit,

            'UNDO': self.undo,
            'REVERSE': self.reverse,
            'REPEAT': self.repeat,
            'COMMUTATOR': self.commutator,
            'CONJUGATE': self.conjugate,
            'SIMPLIFY': self.simplify,
            'INVERT': self.invert,
            'ORIENT': self.orient,

            'INPUT': self.input,
            'LINK': self.link,
            'MOVECOUNT': self.movecount,
            'SPEEDSOLVE': self.speedsolve,
            'SOLVE': self.solve
        }
