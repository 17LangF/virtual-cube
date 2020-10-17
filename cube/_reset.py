'''
Virtual Cube Program - Made by Fred Lang.
Reset method.
'''

import os

#Reset
def reset(self, size='ALL'):
    if type(size) is str:
        if size.upper() == 'ALL':
            self.__init__()
            os.system('cls')
            print()
            return

        if not size.isnumeric():
            raise TypeError
        size = int(size)

    os.system('cls')
    print()

    self.cube = [[[i]*size for x in range(size)] for i in 'ULFRBD']
    self.size = size
    self.moves = []
    self.smoves = []
    zoom = self.showstyle['3D INFO'][3]
    self.showstyle['3D INFO'][4] = abs(zoom) / (5 * size + 10)
