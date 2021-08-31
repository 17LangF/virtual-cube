"""Solve a 3x3 cube using the CFOP or Fridrich method."""

from .ida_star import ida_star


def cfop(self) -> tuple:
    """
    Solve cube using the CFOP or Fridrich method.

    Returns
    -------
    tuple of (list of str, dict of {'3x3 STAGE': int})
        Moves to solve cube, statistics (move count in ETM).

    Notes
    -----
    CFOP consists of 4 steps:
        Cross: solved optimally on the bottom with brute force.
        F2L (First Two Layers): solved with a lookup table.
        OLL (Orientation of the Last Layer): solved with a lookup table.
        PLL (Permutation of the Last Layer): solved with a lookup table.
    """
    solve = []
    stats = {'3x3 STAGE': 0}
    for step in cross, f2l, oll, pll:
        step_solve, _ = step(self)
        solve.extend(step_solve)
        stats['3x3 STAGE'] += len(step_solve)
    return solve, stats


def cross(self) -> tuple:
    """
    Solve cross optimally.

    Returns
    -------
    tuple of (list of str, dict of {'CROSS': int})
        Moves to solve cross, statistics (move count in ETM).

    Notes
    -----
    Using `ida_star`, the cross is solved optimally in 8 moves ETM.
    """
    def estimate(cube):
        cross = [cube[5][y][x] for y, x in ((1,0), (0,1), (1,-1), (-1,1))]
        cross_count = cross.count(cube[5][1][1])
        edges = [side[-1][1] for side in cube[1:5]]
        centres = [side[1][1] for side in cube[1:5]]

        if cross_count == 4:
            if edges == centres:
                return 0
            if ''.join(edges) in ''.join(centres * 2):
                return 1
            if sum(1 for a, b in zip(edges, centres) if a == b) == 2:
                return 5
            return 6

        for s, (y, x) in enumerate(((1,0), (-1,1), (1,-1), (0,1)), 1):
            if (cube[0][y][x] == cube[5][1][1] and
                cube[s][0][1] == cube[s][1][1]):
                minimum = 1
                break
        else:
            for a, b in zip(cube[1:5], cube[2:5] + cube[1:2]):
                if (a[1][-1] == cube[5][1][1] and b[1][0] == b[1][1] or
                    b[1][0] == cube[5][1][1] and a[1][-1] == a[1][1]):
                    minimum = 1
                    break
            else:
                minimum = 2

        if cross_count == 3:
            if any(side[y][1] == cube[5][1][1] for y in (0, -1)
                   for side in cube[1:5]):
                return 3

            for i, cross_edge in enumerate(cross):
                if cross_edge != cube[5][1][1]:
                    break

            if edges[i+1:] + edges[:i] == centres[i+1:] + centres[:i]:
                return minimum
            if ''.join(edges[i+1:] + edges[:i]) in ''.join(centres * 2):
                return 2
            return 3

        if cross_count == 2:
            index = cross.index(cube[5][1][1])
            difference = index - centres.index(edges[index])
            if difference:
                centres = centres[-difference:] + centres[:-difference]

            for cross_edge, edge, centre in zip(cross, edges, centres):
                if cross_edge != cube[5][1][1]:
                    continue
                if edge != centre:
                    return 2 + minimum
            if difference:
                return 3
            return 1 + minimum

        if cross_count == 1:
            index = cross.index(cube[5][1][1])
            difference = centres[index] != edges[index]
            if difference:
                return 4
            return 2 + minimum

        return 3 + minimum

    def next_faces(cube, moves):
        faces = ['U', 'F', 'R', 'L', 'B', 'D']
        cross = (0,1), (1,0), (1,-1), (-1,1)
        if moves:
            face = moves[-1][0]
            if face in faces:
                faces.remove(face)
                if face in {'L', 'B', 'D'}:
                    faces.remove({'L': 'R', 'B': 'F', 'D': 'U'}[face])
        else:
            faces = ((face, f'{face}2', f"{face}'") for face in faces)
            return ('x', 'x2', "x'"), ('z', "z'"), *faces

        if 'U' in faces:
            if (all(cube[5][1][1] != cube[0][y][x] for y, x in cross) and
                all(cube[5][1][1] != side[0][1] for side in cube[1:5])):
                faces.remove('U')

        if 'L' in faces:
            if (all(cube[5][1][1] != cube[1][y][x] for y, x in cross) and
                all(cube[5][1][1] != cube[s][y][x] for s, y, x in
                    ((0,1,0), (2,1,0), (4,1,-1), (5,1,0)))):
                faces.remove('L')

        if 'F' in faces:
            if (all(cube[5][1][1] != cube[2][y][x] for y, x in cross) and
                all(cube[5][1][1] != cube[s][y][x] for s, y, x in
                    ((0,-1,1), (1,1,-1), (3,1,0), (5,0,1)))):
                faces.remove('F')

        if 'R' in faces:
            if (all(cube[5][1][1] != cube[3][y][x] for y, x in cross) and
                all(cube[5][1][1] != cube[s][y][x] for s, y, x in
                    ((0,1,-1), (2,1,-1), (4,1,0), (5,1,-1)))):
                faces.remove('R')

        if 'B' in faces:
            if (all(cube[5][1][1] != cube[4][y][x] for y, x in cross) and
                all(cube[5][1][1] != cube[s][y][x] for s, y, x in
                    ((0,0,-1), (1,1,0), (3,1,-1), (5,-1,1)))):
                faces.remove('B')

        if 'D' in faces:
            if (all(cube[5][1][1] != cube[5][y][x] for y, x in cross) and
                all(cube[5][1][1] != side[-1][1] for side in cube[1:5])):
                faces.remove('D')

        return ((face, f'{face}2', f"{face}'") for face in faces)

    solve = ida_star(self, estimate, next_faces, 8)
    return solve, {'CROSS': len(solve)}


def f2l(self) -> tuple:
    """
    Solve the first two layers (4 corner + edge pairs).

    Returns
    -------
    tuple of (list of str, dict of {'F2L': int})
        Moves to solve F2L, statistics (move count in ETM).

    Notes
    -----
    Each F2L pair is given a 4-digit number. The digits represent: the
    position of the corner (0-7), the orientation of the corner (0-2),
    the position of the edge (0-7), the orientation of the edge (0-1).

    Each number is mirrored depending on which slot the pair should be
    solved into.

    If all 4 numbers are `6060`, F2L is solved.

    16 numbers are made by applying the 4 possible `U` setup moves to
    each of the 4 numbers.

    There are 167 F2L cases and are stored in `docs/F2Ls.txt`. Each line
    has one F2L case with it's 4-digit number and an algorithm which
    solves the pair in the FR slot without any initial `U` moves.

    The file is read through line by line until the 4-digit number in
    the file matches one of the 16 numbers to search for. The algorithm
    which follows the matching number is taken.

    The `U` setup move used to create the number which matched is
    prepended to the algorithm.

    The combined setup move and algorithm is mirrored depending on which
    slot the pair should be solved into to get the final algorithm which
    solves the pair. The algorithm is excecuted, solving one F2L pair.

    This is repeated a maximum of 4 times to solve all 4 F2L pairs.
    """
    cube = self.cube
    size = self.size
    solve = []
    corners = (
        ((0,0,0), (4,0,-1), (1,0,0)),
        ((0,0,-1), (3,0,-1), (4,0,0)),
        ((0,-1,-1), (2,0,-1), (3,0,0)),
        ((0,-1,0), (1,0,-1), (2,0,0)),
        ((5,0,0), (2,-1,0), (1,-1,-1)),
        ((5,0,-1), (3,-1,0), (2,-1,-1)),
        ((5,-1,-1), (4,-1,0), (3,-1,-1)),
        ((5,-1,0), (1,-1,0), (4,-1,-1))
    )
    edges = (
        ((0,0,1), (4,0,1)),
        ((0,1,-1), (3,0,1)),
        ((0,-1,1), (2,0,1)),
        ((0,1,0), (1,0,1)),
        ((2,1,0), (1,1,-1)),
        ((2,1,-1), (3,1,0)),
        ((4,1,0), (3,1,-1)),
        ((4,1,-1), (1,1,0))
    )

    if not hasattr(self, 'f2ls'):
        with open('docs/F2Ls.txt') as f:
            self.f2ls = [line.split(maxsplit=1) for line in f.readlines()]

    for _ in range(4):
        f2l = {pair: [] for pair in ('FR', 'FL', 'BR', 'BL')}
        faces = [side[1][1] for side in cube]

        # Get corner positions and orientations
        for corner in corners:
            stickers = [cube[corner[i][0]][corner[i][1]][corner[i][2]]
                        for i in range(3)]

            if cube[5][1][1] not in stickers:
                continue

            pair = []
            if faces[2] in stickers:
                pair.append('F')
            else:
                pair.append('B')

            if faces[3] in stickers:
                pair.append('R')
            else:
                pair.append('L')
            pair = ''.join(pair)

            if corner[0][0] == 5:
                position = corner[2][0] + 4
            else:
                position = 5 - corner[1][0]

            orientation = stickers.index(cube[5][1][1])

            f2l[pair].extend((position, orientation))

        # Get edge positions and orientations
        for edge in edges:
            stickers = [cube[edge[i][0]][edge[i][1]][edge[i][2]]
                        for i in range(2)]

            if cube[0][1][1] in stickers:
                continue

            pair = []
            if faces[2] in stickers:
                pair.append('F')
            else:
                pair.append('B')

            if faces[3] in stickers:
                pair.append('R')
            else:
                pair.append('L')

            pair = ''.join(pair)

            if edge[0][0] != 0:
                position = 4 + edge[0][0] + edge[1][2]
            else:
                position = 5 - edge[1][0]

            orientation = int(stickers[0] in {faces[1], faces[3]})

            f2l[pair].extend((position, orientation))

        # Correct f2l
        f2l['FL'][0] = (f2l['FL'][0] - 1 ^ 1) + 1
        f2l['FL'][1] = (3 - f2l['FL'][1]) % 3
        if f2l['FL'][2] in {2, 4}:
            f2l['FL'][2] = 6 - f2l['FL'][2]
        elif f2l['FL'][2] > 4:
            f2l['FL'][2] = (f2l['FL'][2] - 1 ^ 1) + 1

        f2l['BR'][0] = (f2l['BR'][0] - 1 ^ 3) + 1
        f2l['BR'][1] = (3 - f2l['BR'][1]) % 3
        if f2l['BR'][2] in {1, 3}:
            f2l['BR'][2] = (f2l['BR'][2] - 1 ^ 2) + 1
        elif f2l['BR'][2] > 4:
            f2l['BR'][2] = 13 - f2l['BR'][2]

        f2l['BL'][0] = (f2l['BL'][0] - 1 ^ 2) + 1
        f2l['BL'][2] = (f2l['BL'][2] - 1 ^ 2) + 1

        if f2l == dict.fromkeys(('FR', 'FL', 'BR', 'BL'), [6, 0, 6, 0]):
            break

        f2ls = [{k: v[:] for k, v in f2l.items()}]
        for _ in range(3):
            for pair in f2l:
                for i in 0, 2:
                    if f2l[pair][i] < 5:
                        f2l[pair][i] = f2l[pair][i] % 4 + 1
            f2ls.append({k: v[:] for k, v in f2l.items()})

        # Find shortest algorithm to solve one F2L pair
        def best_alg():
            for state, alg in self.f2ls:
                for turns in range(4):
                    for pair in f2ls[turns]:
                        if ''.join(map(str, f2ls[turns][pair])) == state:
                            return pair, alg, turns

        pair, alg, turns = best_alg()

        # Correct alg
        if turns:
            if turns == 1:
                setup = 'U'
            elif turns == 2:
                setup = 'U2'
            else:
                setup = "U'"
            alg = f'{setup} {alg}'

        if pair == 'FL':
            replacements = (('U',"U'"), ('u',"u'"), ('D',"D'"), ('y',"y'"),
                            ('R','.'), ('L',"R'"), ('.',"L'"), ('F',"F'"),
                            ("''",''), ("'2", '2'))
        elif pair == 'BR':
            replacements = (('U',"U'"), ('u',"u'"), ('D',"D'"), ('y',"y'"),
                            ('R',"R'"), ('L',"L'"), ('F',"B'"), ("''",''),
                            ("'2", '2'))
        elif pair == 'BL':
            replacements = ('R','.'), ('L','R'), ('.','L'), ('F','B')
        else:
            replacements = ()

        for a, b in replacements:
            alg = alg.replace(a, b)

        if size > 3:
            alg = alg.replace('u', f'{size-1}Uw')

        alg = alg.split()
        self.move(alg)
        solve.extend(alg)

    return solve, {'F2L': len(solve)}


def oll(self) -> tuple:
    """
    Solve the orientation of the last layer.

    Returns
    -------
    tuple of (list of str, dict of {'OLL': int})
        Moves to solve OLL, statistics (move count in ETM).

    Notes
    -----
    The current OLL case is represented as an 8-digit number, each digit
    representing the number of clockwise turns to orient each piece,
    clockwise starting from the top-left.

    If the number is `00000000`, OLL is solved.

    If an odd number of edges are oriented (1 or 3), do the OLL parity
    algorithm: `Rw' U2 Lw F2 Lw' F2 Rw2 U2 Rw U2 Rw' U2 F2 Rw2 F2`. This
    can only happen on even layered cubes. For 6x6 and larger, the wide
    moves have to be changed to adapt to the size of the cube.

    4 numbers are made by applying the 4 possible `U` setup moves to the
    number.

    There are 57 OLL cases and are stored in `docs/OLLs.txt`. Each line
    has one OLL case with it's index number, 8-digit number, and an
    algorithm which solves the OLL without any initial `U` moves.

    The file is read through line by line until the 8-digit number in
    the file matches one of the 4 numbers to search for. The algorithm
    which follows the matching number is taken.

    The `U` setup move used to create the number which matched is
    prepended to the algorithm.

    Any wide moves have to be changed to be adapted to the size of the
    cube and `M` moves must be changed to `m` for big cubes.

    The combined setup move and algorithm is excecuted, solving the OLL.
    """
    cube = self.cube
    size = self.size
    solve = []
    last_layer = (
        ((0,0,0), (4,0,-1), (1,0,0)),
        ((0,0,1), (4,0,1)),
        ((0,0,-1), (3,0,-1), (4,0,0)),
        ((0,1,-1), (3,0,1)),
        ((0,-1,-1), (2,0,-1), (3,0,0)),
        ((0,-1,1), (2,0,1)),
        ((0,-1,0), (1,0,-1), (2,0,0)),
        ((0,1,0), (1,0,1))
    )
    oll = []

    for piece in last_layer:
        for i in range(3):
            if cube[piece[i][0]][piece[i][1]][piece[i][2]] == cube[0][1][1]:
                oll.append(i)
                break

    # OLL parity
    if sum(oll[1::2]) % 2:
        oll_parity = "Rw U2 x Rw U2 Rw U2 Rw' U2 Lw U2 Rw' U2 Rw U2 Rw' U2 Rw'"
        if size > 5:
            rw = f'{size//2}Rw'
            lw = f'{size//2}Lw'
            oll_parity = oll_parity.replace('Rw', rw).replace('Lw', lw)
        oll_parity = oll_parity.split()
        self.move(oll_parity)
        solve.extend(oll_parity)
        oll[3], oll[7] = oll[7], oll[3]
        oll[4], oll[6] = (oll[6] + 1) % 3, (oll[4] - 1) % 3
        oll[5] = 1 - oll[5]

    oll = ''.join(map(str, oll))

    if not hasattr(self, 'olls'):
        with open('docs/OLLs.txt') as f:
            self.olls = [line.split(maxsplit=2) for line in f.readlines()]

    if oll != '00000000':
        olls = [oll[-i:] + oll[:-i] for i in range(0, 8, 2)]
        for _, state, alg in self.olls:
            try:
                turns = olls.index(state)
            except ValueError:
                continue

            if turns:
                if turns == 1:
                    setup = 'U'
                elif turns == 2:
                    setup = 'U2'
                elif turns == 3:
                    setup = "U'"
                alg = f'{setup} {alg}'

            if size > 3:
                alg = alg.replace('f', f'{size-1}Fw')
                alg = alg.replace('r', f'{size-1}Rw')
                alg = alg.replace('M', 'm')

            alg = alg.split()
            self.move(alg)
            solve.extend(alg)
            break

    return solve, {'OLL': len(solve)}


def pll(self) -> tuple:
    """
    The current PLL case is represented as an 8-digit number, each digit
    representing the number of `U` moves to solve each piece, clockwise
    starting from the top-left.

    If the number is `00000000`, PLL is solved.

    If the parity of corners is not equal to the parity of corners, i.e.
    an odd number of piece swaps, do the PLL parity algorithm: `2R2 U2
    2R2 Uw2 2R2 Uw2`. This can only happen on even layered cubes. For
    6x6 and larger, the slice moves and wide moves have to be changed to
    adapt to the size of the cube.

    If the number has four modes (G-permutation) use the mode of the
    digits representing the corner positions. If the number is bimodal
    (H or N permutation), use the first digit of the number as the mode.
    Otherwise the number only has one mode.

    Subtract the mode from each digit of the number modulo 4.

    4 numbers are made by applying the 4 possible `U` setup moves to the
    new number.

    There are 21 PLL cases and are stored in `docs/PLLs.txt`. Each line
    has one PLL case with its name, 8-digit number, and an
    algorithm which solves the PLL without any initial `U` moves.

    The file is read through line by line until the 8-digit number in
    the file matches one of the 4 numbers to search for. The algorithm
    which follows the matching number is taken.

    The `U` setup move used to create the number which matched is
    prepended to the algorithm.

    Any `M` moves must be changed to `m` for big cubes.

    The combined setup move and algorithm is excecuted, solving the PLL.

    If the front layer should be turned to solve the cube, do an `x`
    rotation. If the back layer should be turned to solve the cube, do
    an `x'` rotation.

    Adjust the U face to solve the cube.
    """
    cube = self.cube
    size = self.size
    solve = []
    faces = [side[1][1] for side in cube]
    pll = []

    for s in range(4, 0, -1):
        for x in -1, 1:
            pll.append((s - faces.index(cube[s][0][x])) % 4)

    # PLL Parity
    parity_cases = (
        [0,0,1,3], [0,1,3,0], [1,3,0,0], [3,0,0,1],
        [0,2,0,2], [2,0,2,0], [1,1,1,1], [3,3,3,3],
        [1,2,2,3], [2,2,3,1], [2,3,1,2], [3,1,2,2]
    )

    if (pll[::2] in parity_cases) != (pll[1::2] in parity_cases):
        pll_parity = "2R2 U2 2R2 Uw2 2R2 Uw2"
        if size > 5:
            r = f'2-{size//2}Rw2'
            uw = f'{size//2}Uw'
            pll_parity = pll_parity.replace('2R2', r).replace('Uw', uw)

        pll_parity = pll_parity.split()
        self.move(pll_parity)
        solve.extend(pll_parity)

        for i in 0, 2, 3:
            pll[i], pll[i+4] = pll[i+4] ^ 2, pll[i] ^ 2

    counts = {turn: pll.count(turn) for turn in range(4)}

    if len(set(counts.values())) == 1:
        # G perm
        mode = max(range(4), key=pll[::2].count)
    elif len(set(counts.values())) == 2:
        # H perm / N perm
        mode = pll[0]
    else:
        # Other
        mode = max(set(pll), key=pll.count)

    pll = [(piece - mode) % 4 for piece in pll]
    pll = ''.join(map(str, pll))

    if not hasattr(self, 'plls'):
        with open('docs/PLLs.txt') as f:
            self.plls = [line.split(maxsplit=2) for line in f.readlines()]

    if pll != '00000000':
        plls = [pll[-i:] + pll[:-i] for i in range(0, 8, 2)]
        for _, state, alg in self.plls:
            try:
                turns = plls.index(state)
            except ValueError:
                continue

            if turns:
                if turns == 1:
                    setup = 'U'
                elif turns == 2:
                    setup = 'U2'
                elif turns == 3:
                    setup = "U'"
                alg = f'{setup} {alg}'

            if size > 3:
                alg = alg.replace('M', 'm')

            alg = alg.split()
            self.move(alg)
            solve.extend(alg)
            break

    # AUF
    if cube[0][-2][0] != cube[0][-1][0]:
        self.move('x')
        solve.append('x')
    elif cube[0][0][0] != cube[0][1][0]:
        self.move("x'")
        solve.append("x'")

    if cube[1][0][0] != cube[1][1][1]:
        if cube[2][0][0] == cube[1][1][1]:
            move = 'U'
        elif cube[3][0][0] == cube[1][1][1]:
            move = 'U2'
        else:
            move = "U'"

        self.move(move)
        solve.append(move)

    return solve, {'PLL': len(solve)}
