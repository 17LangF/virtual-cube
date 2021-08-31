"""Set the state of the cube."""

from cube.functions import orient


def input(self, state: str):
    """
    Set the state of the cube.

    Using this may cause problems with other methods.

    Parameters
    ----------
    state : str
        String of all stickers of the cube starting from the U face,
        followed by the L, F, R, B, and D faces, left to right, top to
        bottom. For an NxN cube, `state` should be of length 6 * N^2.

    Raises
    ------
    CubeError
        If the cube state is invalid or not solvable.
    """

    from cube import CubeError

    size = self.size
    mid = size // 2
    state = list(state.upper())

    # Check number of each colour
    if not set(state).issubset('ULFRBD'):
        raise CubeError("At least one character was not in ULFRBD.")

    counts = dict((s, state.count(s)) for s in 'ULFRBD')
    errors = []
    for side in counts:
        if counts[side] > size ** 2:
            errors.append(f"{counts[side] - size ** 2} too many {side}.")
        elif counts[side] < size ** 2:
            errors.append(f"{size ** 2 - counts[side]} too few {side}.")
    errors = '\n'.join(errors)

    if len(state) > size ** 2 * 6:
        raise CubeError(
            f"{errors}\n{len(state) - size ** 2 * 6} too many overall.")
    elif len(state) < size ** 2 * 6:
        raise CubeError(
            f"{errors}\n{size ** 2 * 6 - len(state)} too few overall.")
    else:
        state = [state[y:y + size] for y in range(0, len(state), size)]
        cube = [state[s:s + size] for s in range(0, 6 * size, size)]
        self.cube = cube
        self.smoves = []
        self.moves = []

    # Check if solvable
    if errors:
        raise CubeError(errors)

    # Central centres
    if size % 2:
        centres = [side[mid][mid] for side in cube]
        if set(centres) != {'U', 'L', 'F', 'R', 'B', 'D'}:
            raise CubeError("There are repeated centres.")

        moves = orient(cube)
        if moves:
            self.move(moves)

            centres = [side[mid][mid] for side in cube]
            self.undo(len(moves))

        if centres != ['U', 'L', 'F', 'R', 'B', 'D']:
            raise CubeError("Centres are not in the right position.")

    # Other centres
    if size > 3:
        for y in range(1, mid):
            for x in range(1, (size+1)//2):
                centres = [centre for s in cube for centre in
                           (s[y][x], s[x][-y-1], s[-y-1][-x-1], s[-x-1][y])]

                if any(centres.count(colour) != 4 for colour in 'ULFRBD'):
                    raise CubeError("Centres are not possible.")

    # Corners
    if size > 1:
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
        orientation = 0
        cube_corners = set()
        for corner in corners:
            corner = (cube[corner[0][0]][corner[0][1]][corner[0][2]],
                      cube[corner[1][0]][corner[1][1]][corner[1][2]],
                      cube[corner[2][0]][corner[2][1]][corner[2][2]])

            for colour in 'UD':
                if colour in corner:
                    index = corner.index(colour)
                    break
            else:
                raise CubeError("At least one corner is not possible.")

            if index == 1:
                orientation += 1
                corner = corner[1:] + corner[:1]
            elif index == 2:
                orientation += 2
                corner = corner[2:] + corner[:2]

            if 'U' in corner:
                pair = corner[1:]
            else:
                pair = corner[2], corner[1]

            if ''.join(pair) not in 'LFRBL':
                raise CubeError("At least one corner is not possible.")

            cube_corners.add(corner)

        if len(cube_corners) != 8:
            raise CubeError("There are repeated corners.")

        if orientation % 3:
            raise CubeError("A corner is twisted.")

    # Edges (midges)
    if size > 2 and size % 2:
        edges = (
            ((0,0,mid), (4,0,mid)),
            ((0,mid,-1), (3,0,mid)),
            ((0,-1,mid), (2,0,mid)),
            ((0,mid,0), (1,0,mid)),
            ((2,mid,0), (1,mid,-1)),
            ((2,mid,-1), (3,mid,0)),
            ((4,mid,0), (3,mid,-1)),
            ((4,mid,-1), (1,mid,0)),
            ((5,0,mid), (2,-1,mid)),
            ((5,mid,-1), (3,-1,mid)),
            ((5,-1,mid), (4,-1,mid)),
            ((5,mid,0), (1,-1,mid))
        )
        orientation = 0
        cube_edges = set()
        for edge in edges:
            edge = (cube[edge[0][0]][edge[0][1]][edge[0][2]],
                    cube[edge[1][0]][edge[1][1]][edge[1][2]])

            for colour in 'UDLRFB':
                if colour in edge:
                    index = edge.index(colour)
                    break

            if index == 1:
                orientation += 1
                edge = edge[::-1]

            face = 'ULFDRB'['ULFDRB'.index(edge[0])-3]
            if edge[0] == edge[1] or face == edge[1]:
                raise CubeError("At least one edge is not possible.")

            cube_edges.add(edge)

        if len(cube_edges) != 12:
            raise CubeError("There are repeated edges.")
        if orientation % 2:
            raise CubeError("An edge is flipped.")

    # Edges (wings)
    if size > 3:
        for depth in range(1, mid):
            wings = (
                ((0,0,-depth-1), (4,0,depth)),
                ((0,-depth-1,-1), (3,0,depth)),
                ((0,-1,depth), (2,0,depth)),
                ((0,depth,0), (1,0,depth)),
                ((1,0,-depth-1), (0,-depth-1,0)),
                ((1,-depth-1,-1), (2,-depth-1,0)),
                ((1,-1,depth), (5,-depth-1,0)),
                ((1,depth,0), (4,depth,-1)),
                ((2,0,-depth-1), (0,-1,-depth-1)),
                ((2,-depth-1,-1), (3,-depth-1,0)),
                ((2,-1,depth), (5,0,depth)),
                ((2,depth,0), (1,depth,-1)),
                ((3,0,-depth-1), (0,depth,-1)),
                ((3,-depth-1,-1), (4,-depth-1,0)),
                ((3,-1,depth), (5,depth,-1)),
                ((3,depth,0), (2,depth,-1)),
                ((4,0,-depth-1), (0,0,depth)),
                ((4,-depth-1,-1), (1,-depth-1,0)),
                ((4,-1,depth), (5,-1,-depth-1)),
                ((4,depth,0), (3,depth,-1)),
                ((5,0,-depth-1), (2,-1,-depth-1)),
                ((5,-depth-1,-1), (3,-1,-depth-1)),
                ((5,-1,depth), (4,-1,-depth-1)),
                ((5,depth,0), (1,-1,-depth-1))
            )
            cube_wings = set()
            for wing in wings:
                wing = (cube[wing[0][0]][wing[0][1]][wing[0][2]],
                        cube[wing[1][0]][wing[1][1]][wing[1][2]])
                index = 'ULFDRB'.index(wing[0]) - 3
                if wing[0] == wing[1] or 'ULFDRB'[index] == wing[1]:
                    raise CubeError("At least one wing is not possible.")

                cube_wings.add(wing)

            if len(cube_wings) != 24:
                raise CubeError("There are repeated wings.")
