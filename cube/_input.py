'''
Virtual Cube Program - Made by Fred Lang.
Input method.
'''

#Input
def input(self, state):
    size = self.size

    if len(state) == size ** 2 * 6 and set(state).issubset('ULFRBD'):
        state = list(state.upper())
        state = [state[y:y + size] for y in range(0, len(state), size)]
        self.cube = [state[s:s + size] for s in range(0, 6 * size, size)]
        self.smoves = []
        self.moves = []
        return self.cube
    else:
        raise TypeError
