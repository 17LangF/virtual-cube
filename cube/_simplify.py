"""Simplify moves."""

from cube.functions import orient, split_move, reverse


def simplify(self, *move_types: str) -> list:
    """
    Simplify moves.

    Parameters
    ----------
    *move_types : {'ALL', 'TURNS', 'ADJACENT', 'PARALLEL', 'WIDE',
    'SLICE', 'ROTATION'}
        Move types to simplify.

        TURNS: reduce the number of 90 degree turns.
            e.g., U3 becomes U', U4 U5 U6' U7' becomes U U2 U.
        'ADJACENT': cancel adjacent moves where possible.
            e.g., U U becomes U2, Uw Uw2 becomes Uw'.
        'PARALLEL': cancel moves which are parallel.
            e.g., L R L becomes L2 R, L Lw L becomes L2 Lw.
        'WIDE': remove wide moves and reduce the depth of turns where
        possible.
            e.g., on 3x3, Rw becomes L x. On 5x5, 3Rw becomes Lw x.
        'SLICE': remove slice moves.
            e.g., on 3x3, M becomes L' Lw. On 5x5, 2-3Rw becomes R' 3Rw.
        'ROTATION': move all rotations to the end and simplify them.
            e.g., x U becomes F x, x2 y2 becomes z2.
        'ALL': combine all the above. (Default value if no `move_types`
        given)

        Moves are simplified in the order of SLICE, WIDE, ROTATION,
        PARALLEL, ADJACENT, TURNS.

    Returns
    -------
    list
        Simplified moves.
    """

    from cube import Cube

    moves = self.moves
    size = self.size
    all_move_types = {'TURNS', 'ADJACENT', 'PARALLEL', 'WIDE', 'SLICE',
                      'ROTATION'}
    move_types = ' '.join(move_types).upper().split()

    if not move_types:
        move_types = ['ALL']
    if move_types == ['ALL']:
        move_types = all_move_types

    if not set(move_types).issubset(all_move_types):
        raise ValueError

    suffixes = "0123456789'"

    if 'SLICE' in move_types:
        i = 0
        while i < len(moves):
            depth, face, turns = split_move(moves[i], size)

            if depth[0] != 0 and depth[1] != size:
                moves[i] = face
                if depth[0] > 1:
                    moves[i] += 'w'
                if depth[0] > 2:
                    moves[i] = f'{depth[0]}{moves[i]}'

                if turns % 4 == 1:
                    moves[i] += "'"
                elif turns % 4 == 2:
                    moves[i] += '2'

                moves.insert(i+1, face)

                if depth[1] > 1:
                    moves[i+1] += 'w'
                if depth[1] > 2:
                    moves[i+1] = f'{depth[1]}{moves[i+1]}'

                if turns % 4 == 2:
                    moves[i+1] += '2'
                elif turns % 4 == 3:
                    moves[i+1] += "'"

                i += 1

            i += 1

    if 'WIDE' in move_types:
        i = 0
        while i < len(moves):
            depth, face, turns = split_move(moves[i], size)

            if depth[0] == depth[1]:
                moves.pop(i)
                continue

            if depth[0] > 0 and depth[1] == size:
                depth = [0, size - depth[0]]
                face = 'ULFDRB'['ULFDRB'.index(face)-3]
                moves[i] = f'{depth[1]}{face}w'
                turns = -turns % 4

                if turns == 2:
                    moves[i] += '2'
                elif turns == 3:
                    moves[i] += "'"

            if not depth[0] and depth[1] < size:
                if moves[i][1:2] == '-':
                    moves[i] = moves[i][2:]
                if depth[1] == 1:
                    if moves[i][0] == '1':
                        moves[i] = moves[i][1:].replace('w', '').upper()
                elif depth[1] == 2:
                    if moves[i][0] == '2':
                        moves[i] == moves[i][1:]

            if not depth[0] and size / 2 <= depth[1] < size:
                if depth[1] > size / 2 or face in {'L', 'B', 'D'}:
                    if face in {'U', 'F', 'R'}:
                        if face == 'U':
                            face = 'D'
                            rotation = 'y'
                        elif face == 'F':
                            face = 'B'
                            rotation = 'z'
                        else:
                            face = 'L'
                            rotation = 'x'

                        if turns % 4 == 2:
                            rotation += '2'
                        elif turns % 4 == 3:
                            rotation += "'"

                    else:
                        if face == 'L':
                            face = 'R'
                            rotation = 'x'
                        elif face == 'B':
                            face = 'F'
                            rotation = 'z'
                        else:
                            face = 'U'
                            rotation = 'y'

                        if turns % 4 == 1:
                            rotation += "'"
                        elif turns % 4 == 2:
                            rotation += '2'

                    depth[1] = size - depth[1]
                    moves[i] = face

                    if depth[1] > 1:
                        moves[i] += 'w'
                    if depth[1] > 2:
                        moves[i] = f'{depth[1]}{moves[i]}'
                    if turns % 4 == 2:
                        moves[i] += '2'
                    elif turns % 4 == 3:
                        moves[i] += "'"

                    moves.insert(i+1, rotation)
                    i += 1

            i += 1

    if 'ROTATION' in move_types:
        rotations = []
        i = len(moves) - 1
        while i >= 0:
            depth, face, turns = split_move(moves[i], size)
            if not depth[0] and depth[1] >= size:
                for _ in range(turns % 4):
                    last = ' '.join(moves[i+1:])
                    replacements = {
                        'U': ('LBRF.', 'SM'),
                        'L': ('UFDB.', 'SE'),
                        'F': ('URDL.', 'EM'),
                        'R': ('UBDF.', 'ES'),
                        'B': ('ULDR.', 'ME'),
                        'D': ('LFRB.', 'MS')
                    }
                    faces, slices = replacements[face]

                    for lower in False, True:
                        if lower:
                            faces = faces.lower()
                            slices = slices.lower()

                        for j in range(5):
                            last = last.replace(faces[j], faces[j-1])

                        last = last.replace(slices[0], '.')
                        last = last.replace(slices[1]+"'", slices[0])
                        last = last.replace(slices[1], slices[0]+"'")
                        last = last.replace('.', slices[1])

                    moves[i+1:] = last.split()

                rotations.insert(0, moves[i])
                moves.pop(i)

            i -= 1

        cube = Cube(1)
        cube.move(rotations)
        moves.extend(reverse(orient(cube.cube)))

    if 'PARALLEL' in move_types:
        i = 1
        while i < len(moves):
            depth, face, turns = split_move(moves[i], size)

            if face in {'L', 'B', 'D'}:
                depth = [size - depth[1], size - depth[0]]

                if face == 'L':
                    face = 'R'
                elif face == 'B':
                    face = 'F'
                else:
                    face = 'U'

            for j in range(i-1, -1, -1):
                last_depth, last_face, last_turns = split_move(moves[j], size)
                if last_face in {'L', 'B', 'D'}:
                    last_depth = [size - last_depth[1], size - last_depth[0]]

                    if last_face == 'L':
                        last_face = 'R'
                    elif last_face == 'B':
                        last_face = 'F'
                    else:
                        last_face = 'U'

                if face != last_face:
                    i += 1
                    break

                if depth != last_depth:
                    continue

                moves[j] = moves[j].rstrip(suffixes)
                turn = (last_turns + turns) % 4

                if not turn:
                    moves.pop(i)
                    moves.pop(j)
                    i = j
                    break
                elif turn == 2:
                    moves[j] += '2'
                elif turn == 3:
                    moves[j] += "'"

                moves.pop(i)
                i = j + 1
                break
            else:
                i += 1

    if 'ADJACENT' in move_types:
        i = 1
        while i < len(moves):
            depth, face, turns = split_move(moves[i], size)
            last_depth, last_face, last_turns = split_move(moves[i-1], size)

            if depth == last_depth and face == last_face:
                moves[i-1] = moves[i-1].rstrip(suffixes)
                turns = (turns + last_turns) % 4

                if not turns:
                    moves.pop(i)
                    moves.pop(i-1)
                    i -= 1
                    continue
                elif turns == 2:
                    moves[i-1] += '2'
                elif turns == 3:
                    moves[i-1] += "'"

                moves.pop(i)
                continue

            i += 1

    if 'TURNS' in move_types:
        i = 0
        while i < len(moves):
            depth, face, turns = split_move(moves[i], size)
            moves[i] = moves[i].rstrip(suffixes)
            turns %= 4

            if not turns:
                moves.pop(i)
                continue
            if turns == 2:
                moves[i] += '2'
            elif turns == 3:
                moves[i] += "'"

            i += 1

    return moves
