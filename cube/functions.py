"""Functions which help the cube package."""


def convert_seconds(seconds: float) -> str:
    """
    Convert time in seconds to days:hours:minutes:seconds.milliseconds
    with leading 0s removed.

    Parameters
    ----------
    seconds : float
        Number of seconds to be converted.

    Returns
    -------
    str
        Converted time.
    """
    mS = int((seconds) * 1000)
    D, mS = divmod(mS, 86400000)
    H, mS = divmod(mS, 3600000)
    M, mS = divmod(mS, 60000)
    S, mS = divmod(mS, 1000)
    H = str(H).zfill(2)
    M = str(M).zfill(2)
    S = str(S).zfill(2)
    mS = str(mS).zfill(3)
    time = f'{D}:{H}:{M}:{S}.{mS}'.lstrip('0:')
    if time.startswith('.'):
        time = '0' + time
    return time


def issolved(cube: list) -> bool:
    """
    Return True if the cube is solved, False otherwise.

    A cube is a solved cube if every sticker of each side of the cube is
    the same.
    """
    return all(all(x == s[0][0] for y in s for x in y) for s in cube)


def orient(cube: list):
    """
    Return list of moves which orient the cube, False if not possible.

    For odd layered cubes, a cube is oriented if the white (U) centre is
    facing up, and the green (F) centre is facing the front.

    For even layered cubes, a cube is oriented if the yellow-blue-orange
    (DBL) corner is in the down-back-left (DBL) position correctly
    oriented.
    """
    size = len(cube[0])

    if size % 2:
        mid = size // 2
        centres = [side[mid][mid] for side in cube]
        if {'U', 'F'}.issubset(centres):
            u = centres.index('U')
            f = centres.index('F')
        else:
            return False

    else:
        vertices = (
            ((0,0,0), (4,0,-1), (1,0,0)),
            ((0,0,-1), (3,0,-1), (4,0,0)),
            ((0,-1,-1), (2,0,-1), (3,0,0)),
            ((0,-1,0), (1,0,-1), (2,0,0)),
            ((5,0,0), (2,-1,0), (1,-1,-1)),
            ((5,0,-1), (3,-1,0), (2,-1,-1)),
            ((5,-1,-1), (4,-1,0), (3,-1,-1)),
            ((5,-1,0), (1,-1,0), (4,-1,-1))
        )

        for v in vertices:
            vertex = [cube[v[i][0]][v[i][1]][v[i][2]] for i in range(3)]

            if set(vertex) == set('DBL'):
                u = v[vertex.index('D')][0]
                f = v[vertex.index('B')][0]

                if not u:
                    u = 5
                elif u == 5:
                    u = 0
                else:
                    u = (u + 1) % 4 + 1

                if not f:
                    f = 5
                elif f == 5:
                    f = 0
                else:
                    f = (f + 1) % 4 + 1

    orientations = (
        (False, ["y'"], [], ['y'], ['y2'], False),
        (['z','y'], False, ['z'], False, ['z','y2'], ['z',"y'"]),
        (['x','y2'], ['x',"y'"], False, ['x','y'], False, ['x']),
        (["z'","y'"], False, ["z'"], False, ["z'",'y2'], ["z'",'y']),
        (["x'"], ["x'","y'"], False, ["x'",'y'], False, ["x'",'y2']),
        (False, ['x2',"y'"], ['z2'], ['x2','y'], ['x2'], False)
    )

    return orientations[u][f]


def parse_moves(moves: str) -> list:
    """
    Interpret moves with brackets.

    Grouping: using round brackets, e.g., (R U R' U').
    Repetition: using a number after a bracket, e.g., (R U R' U')3.
    Reversing: using an apostrophe after a bracket, e.g., (R U R' U')'.
    Commutators: using square brackets with a comma, e.g., [R, U].
    Conjugates: using square brackets with a colon, e.g., [R: U].

    Returns
    -------
    list of str
        Moves interpreted.

    Raises
    ------
    MoveError
        If the moves could not be interpreted.
    """

    from cube import MoveError

    # Split joined moves
    i = 0
    previous_move = False
    special_chars = set(' ()[],:')
    move_chars = set('ULFRBDMESXYZ')
    while i < len(moves):
        if moves[i] in special_chars:
            previous_move = False
        elif moves[i].upper() in move_chars:
            if previous_move:
                moves = f'{moves[:i]} {moves[i:]}'
                i += 2
                continue
            else:
                previous_move = True
        i += 1

    # Bracketed moves
    while any(bracket in moves for bracket in '()[]'):
        brackets = []
        for i, char in enumerate(moves):
            if char in {'(', '['}:
                brackets.append((char, i))

            elif char in {')', ']'}:
                if (not len(brackets) or
                    brackets[-1][0] != '(['[')]'.index(char)]):
                    raise MoveError("Brackets are not balanced.")

                bracket = moves[brackets[-1][1]+1: i]

                if char == ']':
                    for separator in {',', ':'}:
                        if bracket.count(separator) == 1:
                            a, b = bracket.split(separator)
                            a = a.strip()
                            b = b.strip()
                            if not (a and b):
                                raise MoveError(
                                    "There must be at least one move on both "
                                    "sides of the separator.")
                            break
                    else:
                        raise MoveError(
                            "Square brackets must contain one comma or one "
                            "colon.")

                    # Commutator
                    if separator == ',':
                        reverse_a = ' '.join(reverse(a.split()))
                        reverse_b = ' '.join(reverse(b.split()))
                        bracket = f'{a} {b} {reverse_a} {reverse_b}'

                    # Conjugate
                    else:
                        reverse_a = ' '.join(reverse(a.split()))
                        bracket = f'{a} {b} {reverse_a}'

                # Repetition
                if i < len(moves) - 1:
                    for end, char in enumerate(moves[i+1:], i+1):
                        if not char.isdecimal():
                            break
                    else:
                        end += 1

                    if end > i + 1:
                        bracket = ' '.join([bracket] * int(moves[i + 1: end]))
                    if end < len(moves):
                        if char == "'":
                            bracket = ' '.join(reverse(bracket.split()))
                            end += 1
                else:
                    end = len(moves)

                moves = moves[:brackets[-1][1]], bracket, moves[end:]
                moves = ' '.join(moves).strip()
                break

        else:
            if len(brackets) != 0:
                raise MoveError("Brackets are not balanced.")

    return moves.split()


def reverse(moves: list) -> list:
    """Return list of reversed moves."""
    reverse = []
    for move in moves[::-1]:
        if move.endswith("'"):
            reverse.append(move[:-1])
        elif move.endswith('2'):
            reverse.append(move)
        else:
            reverse.append(move + "'")
    return reverse


def split_move(move: str, size: int) -> tuple:
    """
    Split move into depth, face, turns.

    Parameters
    ----------
    move : str
        Move to split.

    size : int
        Number of cubies on each edge of the cube.

    Returns
    -------
    tuple of (list of [int, int], str, int)
        A tuple containing:
            depth : list of [int, int]
                Two values marking the start and end of the depth of the
                move. The number of layers being turned is given by
                `depth[1] - depth[0]`.
            face : {'U', 'L', 'F', 'R', 'B', 'D'}
                Centre the turn is rotated about.
            turns : int
                Number of 90 degree rotations of the turn, postive for
                clockwise turns, negative anticlockwise turns.

    Raises
    ------
    MoveError
        If the move is invalid.
    """

    from cube import MoveError

    start_move = move

    # Calculate depth of move

    # Rotations
    if move.startswith(('x', 'y', 'z')):
        depth = [0, size]
        if move.startswith('x'):
            move = 'R' + move[1:]
        elif move.startswith('y'):
            move = 'U' + move[1:]
        else:
            move = 'F' + move[1:]

    # Slice moves
    elif move.upper().startswith(('M', 'E', 'S')):
        if move[0].isupper():
            depth = [size // 2, int(size/2 + 0.5)]
        else:
            depth = [1, size-1]

        if move.upper().startswith('M'):
            move = 'L' + move[1:]
        elif move.upper().startswith('E'):
            move = 'D' + move[1:]
        else:
            move = 'F' + move[1:]

    # Other moves
    elif move[0].isdecimal():
        for i, char in enumerate(move):
            if not char.isdecimal():
                break
        else:
            i += 1

        depth = [0, int(move[:i])]
        move = move[i:]

        if not move:
            raise MoveError(f'"{start_move}" is invalid.')

        if len(move) == 1:
            # e.g., 2U
            if move[0].isupper():
                depth[0] = depth[1] - 1
            # e.g., 2u
            else:
                move = move.capitalize()

        else:
            if move.startswith('-'):
                depth[0] = depth[1] - 1
                move = move[1:]

                if not move[0].isdecimal():
                    raise MoveError(f'"{start_move}" is invalid.')

                for i, char in enumerate(move):
                    if not char.isdecimal():
                        break
                else:
                    i += 1

                depth[1] = int(move[:i])
                move = move[i:]

                if not move:
                    raise MoveError(f'"{start_move}" is invalid.')

                # e.g., 2-3Uw
                if move[0].isupper():
                    if move[1:2] == 'w':
                        move = move[0] + move[2:]
                    else:
                        raise MoveError(f'"{start_move}" is invalid.')
                # e.g., 2-3u
                else:
                    move = move.capitalize()

            elif move[0].isupper():
                # e.g., 2Uw
                if move[1] == 'w':
                    move = move[0] + move[2:]
                # e.g., 2U'
                else:
                    depth[0] = depth[1] - 1
            # e.g., 2u'
            else:
                move = move.capitalize()

    # e.g., u
    elif move[0].islower():
        depth = [0, 2]
        move = move.capitalize()

    else:
        if len(move) > 1:
            # e.g., Uw
            if move[1] == 'w':
                depth = [0, 2]
                move = move[0] + move[2:]
            # e.g., U'
            else:
                depth = [0, 1]
        # e.g., U
        else:
            depth = [0, 1]

    for i in range(2):
        if depth[i] > size:
            depth[i] = size
        elif depth[i] < 0:
            depth[i] = 0
    if depth[1] < depth[0]:
        depth[1] = depth[0]

    # Calculate number of 90 degree turns
    if len(move) > 1:
        # e.g., U2
        if move[1:].isdecimal():
            turns = int(move[1:])
        # e.g., U'
        elif len(move) == 2 and move[1] == "'":
            turns = -1
        # e.g., U2'
        elif move[1:-1].isdecimal() and move[-1] == "'":
            turns = -int(move[1:-1])
        else:
            raise MoveError(f'"{start_move}" is invalid.')
    # e.g., U
    else:
        turns = 1

    face = move[0]
    if face not in {'U', 'L', 'F', 'R', 'B', 'D'}:
        raise MoveError(f'"{start_move}" is invalid.')

    return depth, face, turns
