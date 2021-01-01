'''
Virtual Cube Program - Made by Fred Lang.
Solve module.
'''

from timeit import default_timer

#Import methods
from ._beginners import b_cross, layer1, layer2, eo, co, cp, ep
from ._cage import edges, centres
from ._cfop import cfop, cross, f2l, oll, pll
from ._old_pochmann import op, op_corners, op_edges
from ._optimal import optimal

#Solve
def solve(self, *method):
    size = self.size

    methods = {
        2: {
            'OPTIMAL': optimal,
            'OP': op_corners,
            'OLD POCHMANN': op_corners
        },

        3: {
            'CFOP': (cross, f2l, oll, pll),
            'FRIDRICH': (cross, f2l, oll, pll),
            'BEGINNERS': (b_cross, layer1, layer2, eo, co, cp, ep),
            'OP': op,
            'OLD POCHMANN': op,

            'CROSS': cross,
            'FIRST LAYER': (cross, layer1),
            'F2L': (cross, f2l),
            'OLL': (cross, f2l, oll),
            'EDGES': op_edges,
            'CORNERS': op_corners
        },

        '4+': {
            'CAGE': (edges, centres, cfop),

            'EDGES': edges,
            'CENTRES': centres,
            'REDUCTION': (edges, centres)
        }
    }

    #Find method
    if size > 3:
        size = '4+'

    cubes = 1
    if size in methods:
        if method:
            if isinstance(method[-1], int):
                method, cubes = method[:-1], method[-1]
            elif method[-1].isnumeric():
                method, cubes = method[:-1], int(method[-1])

        if method:
            method = ' '.join(method).upper()
            if method not in methods[size]:
                raise TypeError

        else:
            method = next(iter(methods[size]))
    else:
        return False, {}, 0

    #Solve one cube
    if cubes == 0:
        raise TypeError

    if cubes > 1:
        scramble = self.scramble()

    start_time = default_timer()
    if isinstance(methods[size][method], tuple):
        solve = []
        stats = {}
        for step in methods[size][method]:
            step_solve, step_stats = step(self)
            if step_solve == False:
                return False, {}, 0
            solve.extend(step_solve)
            stats.update(step_stats)
    else:
        solve, stats = methods[size][method](self)
        if solve == False:
            return False, {}, 0

    stats.update(self.movecount(solve))
    stats['TIME'] = default_timer() - start_time

    #If solving more than one cube
    if cubes > 1:
        movecounts = {substep: stats[substep] for substep in stats
                      if isinstance(stats[substep], (int, float))}
        stats = {key: dict(movecounts) for key in ('AVERAGE', 'BEST', 'WORST')}

        for _ in range(cubes-1):
            self.scramble()

            start_solve = default_timer()
            if isinstance(methods[size][method], tuple):
                solve = []
                new_stats = {}
                for step in methods[size][method]:
                    step_solve, step_stats = step(self)
                    if step_solve == False:
                        return False, {}, 0
                    solve.extend(step_solve)
                    new_stats.update(step_stats)
            else:
                solve, new_stats = methods[size][method](self)
                if solve == False:
                    return False, {}, 0

            new_stats.update(self.movecount(solve))
            new_stats['TIME'] = default_timer() - start_solve

            for movecount in movecounts:
                stats['AVERAGE'][movecount] += new_stats[movecount]
                if new_stats[movecount] < stats['BEST'][movecount]:
                    stats['BEST'][movecount] = new_stats[movecount]
                if new_stats[movecount] > stats['WORST'][movecount]:
                    stats['WORST'][movecount] = new_stats[movecount]

        for movecount in movecounts:
            stats['AVERAGE'][movecount] /= cubes
        solve = cubes

    solve_time = default_timer() - start_time

    return solve, stats, solve_time
