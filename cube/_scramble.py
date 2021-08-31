"""Reset and scramble cube with a given scramble or method."""

import random


def scramble(self, *scramble: str):
    """
    Reset and scramble cube with a given scramble or method.

    Parameters
    ----------
    *scramble : str
        Scramble or method to scramble.

        If `scramble` == 'MOVES', cube is scrambled with random moves. A
        number can be passed as the second argument to set the length of
        the scramble. If this is not given, the default scramble lengths
        for NxN cubes are:
            0x0: 25
            1x1: 25
            2x2: 15
            3x3: 25
        For an NxN cube larger than 3x3, the scramble is of length
        20 * (N-2) moves.

        This is the default scramble method if no `scramble` is given.

        If `scramble` == 'STATE', cube is scrambled to a random state.
        This is only possible for 1x1 and 2x2 cubes currently.

        If `scramble` == 'SEED' followed by a second argument, the seed
        given is used to initialise the random number generator.

        Else, `scramble` must be a sequence of moves used to scramble
        the cube.

    Returns
    -------
    list of str or str
        Scramble moves executed on the cube if scrambling else seed if
        initialising a seed.

    Raises
    ------
    CubeError
        If scramble method does not comply with the current cube size.
    MoveError
        If any of the moves are invalid when inputting scramble.
    """

    from cube import CubeError

    size = self.size
    self.reset(size)
    smoves = []
    if not scramble:
        scramble = ['MOVES']

    # Random moves scrambler
    if scramble[0].upper() == 'MOVES':
        if len(scramble) == 1:
            if size == 2:
                length = 15
            elif size in {0, 1, 3}:
                length = 25
            else:
                length = 20 * (size - 2)

        elif len(scramble) == 2 and scramble[1].isdecimal():
             length = int(scramble[1])
        else:
            raise ValueError

        invalid_moves = ['', []]

        while len(smoves) < length:
            # 0x0 scrambler
            if not size:
                smoves = [chr(random.randint(32, 255)) for _ in range(length)]
                return smoves

            # 1x1 scrambler
            if size == 1:
                smove = random.choice('xyz')
                if smove in invalid_moves:
                    continue
                invalid_moves[0] = smove

            # 2x2+ scrambler
            else:
                if size:
                    depth = random.randint(1, size-1)
                else:
                    depth = 1
                smove = random.choice('UFR')

                if smove == invalid_moves[0]:
                    if depth in invalid_moves[1]:
                        continue
                    invalid_moves[1].append(depth)
                else:
                    invalid_moves = [smove, [depth]]

                if depth > size // 2:
                    depth = size - depth
                    if smove == 'U':
                        smove = 'D'
                    elif smove == 'F':
                        smove = 'B'
                    else:
                        smove = 'L'

                if depth > 1:
                    smove += 'w'
                if depth > 2:
                    smove = f'{depth}{smove}'

            smove += random.choice(('', '2', "'"))
            smoves.append(smove)

    # Random state scrambler
    elif scramble[0].upper() == 'STATE':
        # 1x1 scrambler
        if size == 1:
            scramble = [random.choice(('', 'z', 'x', "z'", "x'", 'x2'))]
            scramble.append(random.choice(('', 'y', 'y2', "y'")))

            if scramble == ['', '']:
                scramble = ['x2', 'y2', 'z2']

            for smove in scramble:
                if smove:
                    smoves.append(smove)

        # 2x2 scrambler
        elif size == 2:
            if not hasattr(self, 'solutions'):
                with open('docs/2x2 States and Solutions.txt') as f:
                    self.solutions = {
                        state: solution for line in f.readlines()
                        for state, solution in [line.split(maxsplit=1)]
                    }
            scrambles = list(self.solutions.values())
            del scrambles[0]
            smoves = random.choice(scrambles).split()

        else:
            raise CubeError(
                "Random state scrambler is not available for this size.")

    # Initialise random number generator with seed
    elif scramble[0].upper() == 'SEED':
        seed = ''.join(scramble[1:])
        random.seed(seed)
        return seed

    # Input scramble
    else:
        smoves = list(scramble)

    self.move(smoves)
    self.moves = []
    self.smoves = smoves
    return smoves
