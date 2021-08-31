"""Mirror all previous moves and scramble moves across a plane."""


def mirror(self, plane: str = 'M'):
    """
    Mirror all previous moves and scramble moves across a plane.

    Parameters
    ----------
    plane : {'M', 'E', 'S'}, optional
        Plane the moves are reflected across.

        If `plane` == 'M': the moves are mirrored left to right.
        If `plane` == 'E': the moves are mirrored top to bottom.
        If `plane` == 'S': the moves are mirrored front to back.
    """
    def mirror_moves(moves, swaps, planes):
        mirrored_moves = []
        for move in moves:
            for char, swap in swaps:
                if char in move:
                    move = move.replace(char, swap)
                    break

            if not set(planes).intersection(move):
                if move[-1] == "'":
                    move = move[:-1]
                elif move[-1] != '2':
                    move += "'"

            mirrored_moves.append(move)

        return mirrored_moves

    if plane.upper() == 'M':
        swaps = 'RL', 'LR', 'rl', 'lr'
        planes = 'Mm'
    elif plane.upper() == 'E':
        swaps = 'UD', 'DU', 'ud', 'du'
        planes = 'Ee'
    elif plane.upper() == 'S':
        swaps = 'FB', 'BF', 'fb', 'bf'
        planes = 'Ss'
    else:
        raise ValueError

    moves = self.moves
    smoves = self.smoves
    self.reset(self.size)
    self.smoves = mirror_moves(smoves, swaps, planes)
    self.move(self.smoves)
    self.moves = []
    self.move(mirror_moves(moves, swaps, planes))
