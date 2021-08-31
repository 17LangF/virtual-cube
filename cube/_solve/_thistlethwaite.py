"""Solve cube using Thistlethwaite's algorithm."""

from .ida_star import ida_star
from cube.functions import orient


def g1(self) -> tuple:
    """
    Solve edge orientation.

    Returns
    -------
    tuple of (list of str, dict of {'G1': int})
        Moves to solve edge orientation, statistics (move count in ETM).

    Notes
    -----
    Brute-force method using `ida_star` to solve edge orientation.

    This stage is complete when all 12 edges are correctly oriented. An
    edge is correctly oriented when it can be moved into position in the
    solved orientation without F, F', B, or B' moves.

    This stage takes a maximum of 7 moves and reduces the cube into a
    group requiring only `<U, D, L, R, F2, B2>` moves to solve.
    """
    solve = orient(self.cube)
    self.move(solve)

    edges = (
        ((0, 0, 1), (4, 0, 1)),
        ((0, 1, 0), (1, 0, 1)),
        ((0, 1, -1), (3, 0, 1)),
        ((0, -1, 1), (2, 0, 1)),
        ((2, 1, 0), (1, 1, -1)),
        ((2, 1, -1), (3, 1, 0)),
        ((4, 1, 0), (3, 1, -1)),
        ((4, 1, -1), (1, 1, 0)),
        ((5, 0, 1), (2, -1, 1)),
        ((5, 1, 0), (1, -1, 1)),
        ((5, 1, -1), (3, -1, 1)),
        ((5, -1, 1), (4, -1, 1))
    )

    def get_bad_edges(cube):
        bad_edges = []
        for edge in edges:
            sticker = cube[edge[0][0]][edge[0][1]][edge[0][2]]
            if sticker in {'L', 'R'}:
                bad_edges.append((edge[0][0], edge[1][0]))
            elif sticker in {'F', 'B'}:
                if cube[edge[1][0]][edge[1][1]][edge[1][2]] in {'U', 'D'}:
                    bad_edges.append((edge[0][0], edge[1][0]))
        return bad_edges

    def estimate(cube):
        bad_edges = get_bad_edges(cube)
        if not bad_edges:
            return 0

        total_edges = len(bad_edges)
        edges = [sum(s in edge for edge in bad_edges) for s in (2, 4)]
        minimum = min(edges)
        maximum = max(edges)

        if total_edges == 2:
            return 3 + (maximum != 1)
        if total_edges == 4:
            return 5 - maximum
        if total_edges == 6:
            return 3 + (edges[0] != 3 != edges[1])
        if total_edges == 8:
            if maximum == 4 and minimum < 2:
                return 7 - minimum
            return 6 - minimum
        if total_edges == 10:
            return 6
        return 7

    def next_faces(cube, moves):
        faces = ['F', 'B', 'U', 'R', 'L', 'D']
        if moves:
            face = moves[-1][0]
            faces.remove(face)
            if face in {'L', 'B', 'D'}:
                faces.remove({'L': 'R', 'B': 'F', 'D': 'U'}[face])

        bad_edges = get_bad_edges(cube)
        count = [set() for _ in range(6)]
        for edge in bad_edges:
            count[edge[0]].add(edge[1])
            count[edge[1]].add(edge[0])

        point_symmetry = []
        for face in faces:
            index = 'ULFRBD'.index(face)
            if not count[index]:
                faces.remove(face)
            elif len(count[index]) == 4:
                if face not in {'F', 'B'}:
                    faces.remove(face)
                else:
                    point_symmetry.append(face)
            elif count[index] in ({0,5}, {1,3}, {2,4}):
                point_symmetry.append(face)

        return ((face,) if face in point_symmetry else
                (face, f'{face}2', f"{face}'") for face in faces)

    solve.extend(ida_star(self, estimate, next_faces, 7))
    return solve, {'G1': len(solve)}


def g2(self) -> tuple:
    """
    Solve domino reduction.

    Returns
    -------
    tuple of (list of str, dict of {'G2': int})
        Moves to solve domino reduction, statistics (move count in ETM).

    Notes
    -----
    Brute-force method using `ida_star` to solve domino reduction.

    This stage is complete when both the top and bottom faces only have
    white and yellow (U and D) stickers.

    This stage takes a maximum of 10 moves and reduces the cube into a
    group requiring only `<U, D, L2, R2, F2, B2>` moves to solve.
    """
    def estimate(cube):
        edges = [sum(cube[s][1][x] in {'U', 'D'} for s, x in pieces)
                 for pieces in (((2,0), (4,-1)), ((2,-1), (4,0)))]
        total_edges = sum(edges)

        corners = [sum(side[y][x] in {'U', 'D'} for y in (0, -1) for x in (0, -1))
                   for side in cube[1:5]]
        for i in 0, 1:
            if corners[i+2] < corners[i]:
                corners[i], corners[i+2] = corners[i+2], corners[i]
        total_corners = sum(corners)

        if not total_edges:
            if not total_corners:
                return 0
            return 7

        if total_edges == 1:
            if corners in ([0,1,0,3], [1,0,1,1]):
                return 3
            if corners in ([0,0,2,1], [0,1,0,1], [0,1,0,2], [1,0,2,1]):
                return 5
            return 6

        if total_edges == 2:
            if total_corners == 4:
                if corners == [0,2,0,2]:
                    return 1 + (edges[0] == 1)
                if corners == [1,1,1,1]:
                    return 2 + (edges[0] == 1)
                if corners == [2,0,2,0]:
                    return 3 + (edges[0] == 1)
                return 6

            if not total_corners:
                return 4 + (edges[0] == 1)
            if corners in ([2,1,2,1], [0,4,0,4], [1,2,1,3]):
                return 4 + (edges[0] == 1)
            if corners in ([0,0,0,4], [2,0,2,0]):
                return 4 + (edges[0] != 1)
            return 5

        if total_edges == 3:
            if corners == [0,1,0,3]:
                return 3
            if corners in ([1,0,1,1], [1,1,1,3], [1,2,1,2], [2,1,2,1]):
                return 4
            return 5

        if corners == [0,4,0,4]:
            return 2
        if corners in ([1,2,1,3], [2,2,2,2]):
            return 3
        if corners in ([2,1,2,1], [4,0,4,0]):
            return 4
        return 5

    def next_faces(cube, moves):
        faces = ['R', 'L', 'U', 'D', 'F', 'B']
        if moves:
            face = moves[-1][0]
            faces.remove(face)
            if face in {'L', 'B', 'D'}:
                faces.remove({'L': 'R', 'B': 'F', 'D': 'U'}[face])

        ud = {'U', 'D'}
        point_symmetry = []
        corners = [
            0 if cube[s][y][x] in ud else
            2 if cube[i][s][s] in ud else
            1 for s, y, x, i in (
                (0,0,0,1), (0,-1,0,2), (0,-1,-1,3), (0,0,-1,4),
                (-1,-1,0,4), (-1,0,0,1), (-1,0,-1,2), (-1,-1,-1,3)
            )
        ]

        for face in faces:
            if face == 'U':
                face_corners = corners[:4]
            elif face == 'L':
                face_corners = corners[:2] + corners[5:3:-1]
            elif face == 'F':
                face_corners = corners[1:3] + corners[6:4:-1]
            elif face == 'R':
                face_corners = corners[2:4] + corners[:5:-1]
            elif face == 'B':
                face_corners = [corners[i] for i in (0, 3, 7, 4)]
            else:
                face_corners = corners[4:]

            if face_corners[:2] != face_corners[2:]:
                continue

            s = 'ULFRBD'.index(face)
            if face in {'F', 'B'}:
                y = {2: -1, 4: 0}[s]
                if cube[s][1][0] in ud != cube[s][1][-1] in ud:
                    continue
                if cube[0][y][1] in ud != cube[5][-y-1][1] in ud:
                    continue
                faces.remove(face)

            elif face in {'L', 'R'}:
                y = {1: 0, 3: -1}[s]
                if cube[0][1][y] in ud != cube[5][1][y] in ud:
                    continue
                if cube[2][1][y] in ud != cube[4][1][-y-1] in ud:
                    continue

                if (cube[0][1][y] in ud == cube[2][1][y] in ud and
                    corners[0] == (corners[1] + 1) % 3):
                    faces.remove(face)
                else:
                    point_symmetry.append(face)

            else:
                if cube[s][0][1] in ud != cube[s][-1][1] in ud:
                    continue
                if cube[s][1][0] in ud != cube[s][1][-1] in ud:
                    continue

                if (cube[s][0][1] in ud == cube[s][1][0] in ud and
                    corners[0] == corners[1]):
                    faces.remove('U')
                else:
                    point_symmetry.append('U')

        return ((face,) if face in point_symmetry else
                (f'{face}2',) if face in {'F', 'B'} else
                (face, f'{face}2', f"{face}'") for face in faces)

    solve = ida_star(self, estimate, next_faces, 10)
    return solve, {'G2': len(solve)}


def g3(self) -> tuple:
    """
    Solve half turn reduction.

    Returns
    -------
    tuple of (list of str, dict of {'G3': int})
        Moves to solve half turn reduction, statistics (move count in
        ETM).

    Notes
    -----
    Brute-force method using `ida_star` to solve half turn reduction.

    This stage is complete when every face only contains two coloured
    stickers and every face has an even number of corners of each
    colour.

    This stage takes a maximum of 13 moves and reduces the cube into a
    group requiring only `<U2, D2, L2, R2, F2, B2>` moves to solve.
    """
    def estimate(cube):
        faces = 'FB', 'LR', 'FB', 'LR'
        edges = [sum(cube[s][y][1] in face for s, face in enumerate(faces, 1))
                 for y in (0, -1)]
        total_edges = sum(edges)
        corners = [sum(cube[s][y][x] in {'F', 'B'} for s in (1, 3)
                       for x in (0, -1)) for y in (0, -1)]
        total_corners = sum(corners)

        if not total_corners:
            if any(sum(side[y][x] == side[1][1] for y in (0, -1)
                       for x in (0, -1)) % 2 for side in cube[:3]):
                return 10
            if any(sum(cube[s][y][0] == cube[s][y][-1] for s in opposite) % 2
                   for y in (0, -1) for opposite in ((0,5), (1,3), (2,4))):
                return 9
            if not total_edges:
                return 0
            if total_edges == 2:
                return 5
            if total_edges == 4:
                return 4
            if total_edges == 6:
                return 7
            return 6

        if total_corners == 2:
            if total_edges == 2:
                return 5
            return 6

        if total_corners == 4:
            if max(corners) == 4:
                if total_edges == 4:
                    if corners == edges:
                        return 1
                    if max(edges) == 4:
                        return 5
                    if edges[0] == 2:
                        return 3
                    return 4
                return 7

            if max(corners) == 3:
                return 4
            if total_edges == 4:
                return 2
            return 3

        if total_corners == 6:
            if corners[0] == 3:
                return 5
            return 6

        if total_edges == 8:
            return 2
        if total_edges == 4:
            return 4
        if not total_edges:
            return 6
        return 5

    def next_faces(cube, moves):
        faces = ['U', 'D', 'R', 'L', 'F', 'B']
        if moves:
            face = moves[-1][0]
            faces.remove(face)
            if face in {'L', 'B', 'D'}:
                faces.remove({'L': 'R', 'B': 'F', 'D': 'U'}[face])

        point_symmetry = []
        edges = [side[y][1] in {'F', 'B'} for y in (0, -1)
                 for side in cube[1:5]]
        corners = [cube[s][y][x] in {'F', 'B'} for y in (0, -1) for s in (1, 3)
                   for x in (0, -1)]

        for face in faces:
            if face in {'U', 'D'}:
                s = {'U': 0, 'D': 4}[face]
                if edges[s:s+2] != edges[s+2:s+4]:
                    continue
                if corners[s:s+2] != corners[s+2:s+4]:
                    continue

                if edges[s] == edges[s+1] and corners[s] != corners[s+1]:
                    faces.remove(face)
                else:
                    point_symmetry.append(face)

            else:
                s = 'LFRB'.index(face)
                if edges[s] != edges[s+4]:
                    continue
                if corners[s] != corners[(s+1)%4+4]:
                    continue
                if corners[(s+1)%4] != corners[(s-1)%4+4]:
                    continue
                faces.remove(face)

        return ((face,) if face in point_symmetry else
                (face, f'{face}2', f"{face}'") if face in {'U', 'D'} else
                (f'{face}2',) for face in faces)

    solve = ida_star(self, estimate, next_faces, 13)
    return solve, {'G3': len(solve)}


def g4(self) -> tuple:
    """
    Solve half turn only state.

    Returns
    -------
    tuple of (list of str, dict of {'G4': int})
        Moves to solve half turn only state, statistics (move count in
        ETM).

    Notes
    -----
    Brute-force method using `ida_star` to solve half turn only state.

    This stage takes a maximum of 15 moves and solves the cube.
    """
    def estimate(cube):
        axes = (
            [cube[s][y if s != 4 else -y-1][1] != cube[s][1][1]
             for s in (0, 2, 5, 4) for y in (0, -1)],
            [side[1][x] != side[1][1] for side in cube[1:5] for x in (0, -1)],
            [cube[s][y][x] != cube[s][1][1]
             for s, y, x in ((0,1,0), (0,1,-1), (3,0,1), (3,-1,1),
                             (5,1,-1), (5,1,0), (1,-1,1), (1,0,1))]
        )
        edges = []

        for axis in axes:
            count = sum(axis)
            if count == 2:
                edges.append(1)
            elif count == 4:
                if not sum(axis[::2]) % 4:
                    edges.append(3)
                elif not (sum(axis[i] for i in (1, 2, 5, 6))) % 4:
                    edges.append(3)
                else:
                    edges.append(2)
            elif count == 6:
                edges.append(3)
            elif count == 8:
                edges.append(4)
            else:
                edges.append(0)

        corners = [[side[y][x] != side[1][1] for y in (0, -1) for x in (0, -1)]
                   for side in cube[:3]]
        count = sum(sum(side) for side in corners)

        if count == 4:
            if [0, 1, 1, 0] in corners or [1, 0, 0, 1] in corners:
                if sorted(edges) == [1, 2, 3]:
                    if edges[(1 - corners.index([0, 0, 0, 0])) % 3] == 3:
                        return 4
                return 6
            if corners[0] == corners[2]:
                if edges == [0, 1, 1]:
                    if corners[0][0]:
                        if axes[1][2] and axes[2][0]:
                            return 1
                    else:
                        if axes[1][3] and axes[2][1]:
                            return 1
                return 5
            if corners[1] == corners[2]:
                if edges == [1, 0, 1]:
                    if corners[1][0]:
                        if axes[0][2] and axes[2][2]:
                            return 1
                    else:
                        if axes[0][3] and axes[2][3]:
                            return 1
                return 5
            if corners[0] == [corners[1][i] for i in (0, 2, 1, 3)]:
                if edges == [1, 1, 0]:
                    if corners[0][0]:
                        if axes[0][0] and axes[1][0]:
                            return 1
                    else:
                        if axes[0][1] and axes[0][1]:
                            return 1
                return 5
            if sorted(edges) == [0, 1, 3]:
                if edges[(1 - corners.index([0, 0, 0, 0])) % 3] == 3:
                    return 3
            return 5

        if count == 6:
            if [0, 1, 1, 0] in corners or [1, 0, 0, 1] in corners:
                return 3 if edges == [2, 2, 2] else 5
            return 2 if sorted(edges) == [1, 1, 2] else 4

        if count == 8:
            if [0, 0, 0, 0] in corners:
                if sorted(edges) == [0, 2, 2]:
                    if not edges[(1 - corners.index([0, 0, 0, 0])) % 3]:
                        return 2
                return 4
            if [0, 1, 1, 0] in corners or [1, 0, 0, 1] in corners:
                return 4 if sorted(edges) == [2, 3, 3] else 5
            return 3 if sorted(edges) == [1, 2, 3] else 5

        return 0 if edges == [0, 0, 0] else 6

    def next_faces(_, moves):
        faces = ['U', 'D', 'R', 'L', 'F', 'B']
        if moves:
            face = moves[-1][0]
            faces.remove(face)
            if face in {'L', 'B', 'D'}:
                faces.remove({'L': 'R', 'B': 'F', 'D': 'U'}[face])

        return ((f'{face}2',) for face in faces)

    solve = ida_star(self, estimate, next_faces, 15)
    return solve, {'G4': len(solve)}
