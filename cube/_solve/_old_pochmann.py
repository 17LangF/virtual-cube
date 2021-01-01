'''
Virtual Cube Program - Made by Fred Lang.
Old Pochmann solver.
'''

from cube.functions import reverse

#Old Pochmann
def op(self):
    solve, stats = op_edges(self)

    if len(stats['EDGE MEMO']) % 3 == 1:
        parity_alg = "R U' R' U' R U R D R' U' R D' R' U2 R' U'".split()

        self.move(parity_alg)
        solve.extend(parity_alg)

        stats['PARITY'] = 'ODD'
    else:
        stats['PARITY'] = 'EVEN'

    step_solve, step_stats = op_corners(self)
    solve.extend(step_solve)
    stats.update(step_stats)

    return solve, stats

#Old Pochmann corners
def op_corners(self):
    cube = self.cube
    size = self.size
    solve = []
    stats = {}

    if size > 2:
        faces = [side[1][1] for side in cube]
    else:
        faces = 'ULFRBD'

    corners = {
        'A': ((0,0,0), (4,0,-1), (1,0,0), "BUFFER"),
        'B': ((0,0,-1), (3,0,-1), (4,0,0), "R D'"),
        'C': ((0,-1,-1), (2,0,-1), (3,0,0), 'F'),
        'D': ((0,-1,0), (1,0,-1), (2,0,0), "F R'"),
        'E': ((1,0,0), (0,0,0), (4,0,-1), 'BUFFER'),
        'F': ((1,0,-1), (2,0,0), (0,-1,0), 'F2'),
        'G': ((1,-1,-1), (5,0,0), (2,-1,0), "F2 R'"),
        'H': ((1,-1,0), (4,-1,-1), (5,-1,0), 'D2'),
        'I': ((2,0,0), (0,-1,0), (1,0,-1), "F' D"),
        'J': ((2,0,-1), (3,0,0), (0,-1,-1), 'F2 D'),
        'K': ((2,-1,-1), (5,0,-1), (3,-1,0), 'F D'),
        'L': ((2,-1,0), (1,-1,-1), (5,0,0), 'D'),
        'M': ((3,0,0), (0,-1,-1), (2,0,-1), "R'"),
        'N': ((3,0,-1), (4,0,0), (0,0,-1), 'R2'),
        'O': ((3,-1,-1), (5,-1,-1), (4,-1,0), 'R'),
        'P': ((3,-1,0), (2,-1,-1), (5,0,-1), ''),
        'Q': ((4,0,0), (0,0,-1), (3,0,-1), "R' F"),
        'R': ((4,0,-1), (1,0,0), (0,0,0), 'BUFFER'),
        'S': ((4,-1,-1), (5,-1,0), (1,-1,0), "D' R"),
        'T': ((4,-1,0), (3,-1,-1), (5,-1,-1), "D'"),
        'U': ((5,0,0), (2,-1,0), (1,-1,-1), "F'"),
        'V': ((5,0,-1), (3,-1,0), (2,-1,-1), "F' R'"),
        'W': ((5,-1,-1), (4,-1,0), (3,-1,-1), "D2 F'"),
        'X': ((5,-1,0), (1,-1,0), (4,-1,-1), "D F'")
    }

    corner = 'A'
    corner_memo = []
    solved_corners = []

    while len(solved_corners) < 21:
        corner = corners[corner]
        corner = (cube[corner[0][0]][corner[0][1]][corner[0][2]],
                  cube[corner[1][0]][corner[1][1]][corner[1][2]],
                  cube[corner[2][0]][corner[2][1]][corner[2][2]])
        corner = tuple(faces.index(i) for i in corner)

        for possible_corner in corners:
            if (tuple(corners[possible_corner][i][0] for i in range(3))
                == corner):
                corner = possible_corner
                break

        #New cycle
        if corners[corner][3] == 'BUFFER':
            for possible_corner in corners:
                if corners[possible_corner][3] == 'BUFFER':
                    continue

                if corners[possible_corner][0] not in solved_corners:
                    corner = possible_corner
                    break

        #End cycle
        elif corners[corner][0] in solved_corners:
            corner_memo.append(corner)
            for possible_corner in corners:
                if corners[possible_corner][3] == 'BUFFER':
                    continue

                if corners[possible_corner][0] not in solved_corners:
                    corner = possible_corner
                    break

        solved_corners.extend(corners[corner][:3])
        corner_memo.append(corner)

    corner = corners[corner]
    corner = (cube[corner[0][0]][corner[0][1]][corner[0][2]],
              cube[corner[1][0]][corner[1][1]][corner[1][2]])
    corner = tuple(faces.index(i) for i in corner)

    for possible_corner in corners:
        if tuple(corners[possible_corner][i][0] for i in [0,1]) == corner:
            corner = possible_corner
            break

    if corner != 'A':
        corner_memo.append(corner)

    i = 0
    while i < len(corner_memo) - 1:
        if corner_memo[i] == corner_memo[i+1]:
            corner_memo = corner_memo[:i] + corner_memo[i+2:]
        else:
            i += 1

    corner_alg = "R U' R' U' R U R' F' R U R' U' R' F R".split()

    for corner in corner_memo:
        setup = corners[corner][3].split()

        if not setup:
            solve.extend(corner_alg)
            continue

        solve.extend(setup)
        solve.extend(corner_alg)
        solve.extend(reverse(setup))

    if size > 3:
        solve = [f'{size-1}{move}' if 'w' in move else move for move in solve]

    self.move(solve)

    stats['OP CORNERS'] = len(solve)

    corner_memo = iter(corner_memo)
    corner_memo = [letter + next(corner_memo,'') for letter in corner_memo]

    stats['CORNER MEMO'] = ' '.join(corner_memo)

    return solve, stats

#Old Pochmann edges
def op_edges(self):
    cube = self.cube
    size = self.size
    solve = []
    stats = {}

    faces = [side[1][1] for side in cube]

    edges = {
        'A': ((0,0,1), (4,0,1), "Lw2 D' L2"),
        'B': ((0,1,-1), (3,0,1), 'BUFFER'),
        'C': ((0,-1,1), (2,0,1), 'Lw2 D L2'),
        'D': ((0,1,0), (1,0,1), ''),
        'E': ((1,0,1), (0,1,0), "L Dw' L"),
        'F': ((1,1,-1), (2,1,0), "Dw' L"),
        'G': ((1,-1,1), (5,1,0), "L' Dw' L"),
        'H': ((1,1,0), (4,1,-1), "Dw L'"),
        'I': ((2,0,1), (0,-1,1), "Lw D' L2"),
        'J': ((2,1,-1), (3,1,0), 'Dw2 L'),
        'K': ((2,-1,1), (5,0,1), 'Lw D L2'),
        'L': ((2,1,0), (1,1,-1), "L'"),
        'M': ((3,0,1), (0,1,-1), 'BUFFER'),
        'N': ((3,1,-1), (4,1,0), 'Dw L'),
        'O': ((3,-1,1), (5,1,-1), "D' Lw D L2"),
        'P': ((3,1,0), (2,1,-1), "Dw' L'"),
        'Q': ((4,0,1), (0,0,1), "Lw' D L2"),
        'R': ((4,1,-1), (1,1,0), 'L'),
        'S': ((4,-1,1), (5,-1,1), "Lw' D' L2"),
        'T': ((4,1,0), (3,1,-1), "Dw2 L'"),
        'U': ((5,0,1), (2,-1,1), "D' L2"),
        'V': ((5,1,-1), (3,-1,1), 'D2 L2'),
        'W': ((5,-1,1), (4,-1,1), 'D L2'),
        'X': ((5,1,0), (1,-1,1), 'L2')
    }

    edge = 'B'
    edge_memo = []
    solved_edges = []

    while len(solved_edges) < 22:
        edge = edges[edge]
        edge = (cube[edge[0][0]][edge[0][1]][edge[0][2]],
                cube[edge[1][0]][edge[1][1]][edge[1][2]])
        edge = tuple(faces.index(i) for i in edge)

        for possible_edge in edges:
            if tuple(edges[possible_edge][i][0] for i in [0,1]) == edge:
                edge = possible_edge
                break

        #New cycle
        if edges[edge][2] == 'BUFFER':
            for possible_edge in edges:
                if edges[possible_edge][2] == 'BUFFER':
                    continue

                if edges[possible_edge][0] not in solved_edges:
                    edge = possible_edge
                    break

        #End cycle
        elif edges[edge][0] in solved_edges:
            edge_memo.append(edge)
            for possible_edge in edges:
                if edges[possible_edge][2] == 'BUFFER':
                    continue

                if edges[possible_edge][0] not in solved_edges:
                    edge = possible_edge
                    break

        solved_edges.extend(edges[edge][:2])
        edge_memo.append(edge)

    edge = edges[edge]
    edge = (cube[edge[0][0]][edge[0][1]][edge[0][2]],
            cube[edge[1][0]][edge[1][1]][edge[1][2]])
    edge = tuple(faces.index(i) for i in edge)

    for possible_edge in edges:
        if tuple(edges[possible_edge][i][0] for i in [0,1]) == edge:
            edge = possible_edge
            break

    if edge != 'B':
        edge_memo.append(edge)

    i = 0
    while i < len(edge_memo) - 1:
        if edge_memo[i] == edge_memo[i+1]:
            edge_memo = edge_memo[:i] + edge_memo[i+2:]
        else:
            i += 1

    edge_alg = "R U R' U' R' F R2 U' R' U' R U R' F'".split()

    for edge in edge_memo:
        setup = edges[edge][2].split()

        if not setup:
            solve.extend(edge_alg)
            continue

        solve.extend(setup)
        solve.extend(edge_alg)
        solve.extend(reverse(setup))

    if size > 3:
        solve = [f'{size-1}{move}' if 'w' in move else move for move in solve]

    self.move(solve)

    stats['OP EDGES'] = len(solve)

    edge_memo = iter(edge_memo)
    edge_memo = [letter + next(edge_memo,'') for letter in edge_memo]

    stats['EDGE MEMO'] = ' '.join(edge_memo)

    return solve, stats
