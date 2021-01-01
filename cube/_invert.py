'''
Virtual Cube Program - Made by Fred Lang.
Invert method.
'''

from cube.functions import reverse

#Invert
def invert(self):
    size = self.size
    smoves = self.smoves
    moves = self.moves
    self.reset(self.size)

    self.smoves = reverse(moves)
    self.move(self.smoves)
    self.moves = []
    self.move(reverse(smoves))
