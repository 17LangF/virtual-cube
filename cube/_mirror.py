'''
Virtual Cube Program - Made by Fred Lang.
Mirror method.
'''

#Mirror
def mirror(self, slice='M'):
    def mirror_moves(moves, swaps, slices):
        mirror = []
        for move in moves:
            for char, swap in swaps:
                if char in move:
                    move = move.replace(char, swap)
                    break

            if not set(slices).intersection(move):
                if move[-1] == "'":
                    move = move[:-1]
                elif move[-1] != '2':
                    move += "'"

            mirror.append(move)

        return mirror

    if slice.upper() == 'M':
        swaps = 'RL', 'LR', 'rl', 'lr'
        slices = 'Mm'
    elif slice.upper() == 'E':
        swaps = 'UD', 'DU', 'ud', 'du'
        slices = 'Ee'
    elif slice.upper() == 'S':
        swaps = 'FB', 'BF', 'fb', 'bf'
        slices = 'Ss'
    else:
        raise TypeError

    moves = self.moves
    smoves = self.smoves
    self.reset(self.size)

    self.smoves = mirror_moves(smoves, swaps, slices)
    self.move(self.smoves)
    self.moves = []
    self.move(mirror_moves(moves, swaps, slices))
