"""Package which solves cube using dfferent methods."""

from timeit import default_timer

from ._beginners import b_cross, layer1, layer2, eo, co, cp, ep
from ._cage import edges, centres
from ._cfop import cfop, cross, f2l, oll, pll
from ._old_pochmann import op, op_corners, op_edges
from ._optimal import optimal_2x2, optimal_nxn
from ._thistlethwaite import g1, g2, g3, g4


def solve(self, *method: str, cubes: int = 1) -> tuple:
    """
    Compute a solution to solve the cube using a given method.

    Parameters
    ----------
    *method : str
        Method used to solve. If the last argument is an integer or
        numeric string, the integer value is assigned to `cubes`, and
        the cube will be scrambled and solved that many times.
    cubes : int, default=1
        Number of cubes to solve.

    Returns
    -------
    tuple
        If solving only the current cube, the tuple contains:
            moves : list of str
                Moves to solve the cube.
            stats : dict
                Statistics of the solve.

        Otherwise, the tuple contains:
            cubes : int
                Number of cubes scrambled and solved.
            stats : tuple of (list of dict, float)
                Statistics of each cube, solve time in seconds.

        Statistics include:
            MOVECOUNT:  move count of solve in HTM, QTM, STM, and ETM.
            TIME: time the program took to find a solution.

            The move count in ETM for each substep in the method.

            For Old Pochmann, the piece swaps are described using the
            Speffz letter scheme.

    Raises
    ------
    CubeError
        If any cube was not solvable.

    Notes
    -----
    Methods for different cube sizes:

    2x2 - OPTIMAL
        Solve cube in the fewest moves (HTM). Solutions are 3-gen, so
        only use U, F, and R moves. Note: the first solve will be
        significantly slower than average for the program to read the
        file.

    2x2 - OP or OLD POCHMANN
        Solve cube using setup moves and swaps. Corners are solved using
        an altered Y-permutation with buffer at A.

    3x3 - CFOP or FRIDRICH
        Solve cube using the CFOP or Fridrich method. The cross is
        solved on the bottom face.

    3x3 - BEGINNERS
        Solve cube using a beginner's method.

    3x3 - OP or OLD POCHMANN
        Solve cube using setup moves and swaps. Edges are solved using
        the T-permutation with buffer at B. Parity is solved using the
        Ra-permutation. Corners are solved using an altered
        Y-permutation with buffer at A.

    3x3 - THISTLETHWAITE
    Solve cube using Thistlethwaite's algorithm.

    3x3 - OPTIMAL
        Solve cube in as few moves as possible. The more moves required
        to solve, the longer it will take to find a solution.

    3x3 Substeps:
        CROSS: cross
        FIRST LAYER: cross, first layer corners
        F2L: cross, F2L
        OLL: cross, F2L, OLL
        CORNERS: Old Pochmann corners
        EDGES: Old Pochmann edges
        EDGE ORIENTATION: g1
        DOMINO REDUCTION: g1, g2
        HALF TURN REDUCTION: g1, g2, g3

    4x4+ - CAGE
        Solve cube by solving edges first, using commutators to solve
        centres, and then solving the cube as a 3x3 using CFOP.

    4x4+ - OPTIMAL
        Solve cube in as few moves as possible. The more moves required
        to solve, the longer it will take to find a solution.

    4x4+ Substeps:
        EDGES: edges
        CENTRES: centres preserving edges
        REDUCTION: edges, centres
    """

    from cube import CubeError

    size = self.size
    methods = {
        2: {
            'OPTIMAL': optimal_2x2,
            'OP': op_corners,
            'OLD POCHMANN': op_corners,
        },

        3: {
            'CFOP': (cross, f2l, oll, pll),
            'FRIDRICH': (cross, f2l, oll, pll),
            'BEGINNERS': (b_cross, layer1, layer2, eo, co, cp, ep),
            'OP': op,
            'OLD POCHMANN': op,
            'OPTIMAL': optimal_nxn,
            'THISTLETHWAITE': (g1, g2, g3, g4),

            'CROSS': cross,
            'FIRST LAYER': (cross, layer1),
            'F2L': (cross, f2l),
            'OLL': (cross, f2l, oll),
            'EDGES': op_edges,
            'CORNERS': op_corners,

            'EDGE ORIENTATION': g1,
            'DOMINO REDUCTION': (g1, g2),
            'HALF TURN REDUCTION': (g1, g2, g3)
        },

        '4+': {
            'CAGE': (edges, centres, cfop),
            'OPTIMAL': optimal_nxn,

            'EDGES': edges,
            'CENTRES': centres,
            'REDUCTION': (edges, centres)
        }
    }

    if size > 3:
        size = '4+'
    if size not in methods:
        raise CubeError("Could not solve.")

    scramble = cubes > 1

    if method:
        if isinstance(method[-1], int):
            method, cubes = method[:-1], method[-1]
            scramble = True
        elif method[-1].isdecimal():
            method, cubes = method[:-1], int(method[-1])
            scramble = True

    if method:
        method = ' '.join(method).upper()
        if method not in methods[size]:
            raise ValueError
    else:
        method = next(iter(methods[size]))

    if not cubes:
        raise ValueError

    start_time = default_timer()
    stats = []

    for _ in range(cubes):
        if scramble:
            self.scramble()
        start_solve = default_timer()
        if isinstance(methods[size][method], tuple):
            solve = []
            new_stats = {}
            for step in methods[size][method]:
                step_solve, step_stats = step(self)
                if step_solve == False:
                    raise CubeError("Could not solve.")
                solve.extend(step_solve)
                new_stats.update(step_stats)
        else:
            solve, new_stats = methods[size][method](self)
            if solve == False:
                raise CubeError("Could not solve.")

        new_stats.update(self.movecount(solve))
        new_stats['TIME'] = default_timer() - start_solve
        stats.append(new_stats)

    if not scramble:
        return solve, new_stats

    solve_time = default_timer() - start_time
    return cubes, (stats, solve_time)
