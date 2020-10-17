'''
Virtual Cube Program - Made by Fred Lang.
Invert method.
'''

import os

#Invert
def invert(self):
    size = self.size
    smoves = self.smoves
    moves = self.moves
    self.cube = [[[i]*size for x in range(size)] for i in 'ULFRBD']

    if moves:
        self.scramble(*self.reverse(moves))
    else:
        os.system('cls')
        print()
        self.smoves = []

    for move in self.reverse(smoves):
        self.move(move)
