'''
Virtual Cube Program - Made by Fred Lang.
Solve class.
'''

from timeit import default_timer

#Import methods
from ._beginners import cross, layer1, layer2, eo, co, cp, ep
from ._cage import centres
from ._old_pochmann import op, op_corners, op_edges
from ._optimal import optimal

#Solve
def solve(self, *method):
    start_time = default_timer()

    cube = self.cube
    size = self.size
    method = ' '.join(method).upper()

    if all(all(x == s[0][0] for y in s for x in y) for s in cube):
        return [], {}, default_timer() - start_time

    methods = {
        2: {
            'OPTIMAL': optimal,
            'OP': op_corners,
            'OLD POCHMANN': op_corners
        },

        3: {
            'BEGINNERS': (cross, layer1, layer2,
                          eo, co, cp, ep),
            'OP': op,

            'OP CORNERS': op_corners,
            'CROSS': cross,
            'FIRST LAYER': (cross, layer1),
            'SECOND LAYER': (cross, layer1, layer2),
            'LAST LAYER CROSS': (cross, layer1, layer2,
                                 eo),
            'LAST LAYER FACE': (cross, layer1, layer2,
                                eo, co),
            'LAST LAYER CORNERS': (cross, layer1, layer2,
                                   eo, co, cp),
            'OLD POCHMANN': op,
            'OP EDGES': op_edges
        },

        '4+': {
            'CENTRES': centres
        }
    }

    if size > 3:
        size = '4+'

    if size in methods:
        if method:
            if method not in methods[size]:
                raise TypeError
        else:
            method = next(iter(methods[size]))
    else:
        return False, {}, 0

    if type(methods[size][method]) is tuple:
        solve = []
        stats = {}
        for step in methods[size][method]:
            step_solve, step_stats = step(self)
            solve.extend(step_solve)
            stats.update(step_stats)
    else:
        solve, stats = methods[size][method](self)

    if method not in ('OP', 'OLD POCHMANN', 'OP EDGES', 'OP CORNERS',
        'OPTIMAL'):
        if solve:
            self.undo(len(solve))

    for stat in stats:
        if not stats[stat]:
            stats[stat] = 'None'

    time = default_timer() - start_time

    return solve, stats, time
