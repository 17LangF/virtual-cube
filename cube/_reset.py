'''
Virtual Cube Program - Made by Fred Lang.
Reset method.
'''

#Reset
def reset(self, size='ALL'):
    if isinstance(size, str):
        if size.upper() == 'ALL':
            self.__init__()
            return

        if not size.isnumeric():
            raise TypeError
        size = int(size)

    self.cube = [[[i]*size for _ in range(size)] for i in 'ULFRBD']
    self.moves = []
    self.smoves = []

    if size != self.size:
        self.size = size
        zoom = self.showstyle['3D'][3]
        self.showstyle['3D'][4] = abs(zoom) / (5 * size + 5)
