'''
Virtual Cube Program - Made by Fred Lang.
Speedsolve method.
'''

import os
import time
from timeit import default_timer

from cube.functions import convert_seconds, issolved, parse_moves

#Speedsolve
def speedsolve(self):
    from cube import Cube

    self.scramble()

    os.system('cls')
    print()
    self.show()

    start = default_timer()
    inspection = True

    while not issolved(self.cube):
        moves = input('\nEnter move(s): ').strip()
        os.system('cls')

        if inspection:
            if default_timer() > start + 15:
                start_time = start + 15
                inspection = False

        if moves.upper() == 'EXIT':
            break

        elif moves.upper() == 'TIME':
            if inspection:
                solve_time = convert_seconds(default_timer() - start)
                print(f'INSPECTION: {solve_time}')
            else:
                solve_time = convert_seconds(default_timer() - start_time)
                print(f'TIME: {solve_time}')

            print()
            self.show()
            continue

        if inspection:
            start_time = default_timer()
            inspection = False

        try:
            moves = parse_moves(moves)
            self.move(moves)
        except Cube.MoveError as e:
            print(e)

        print()
        self.show()

    end = default_timer()

    if inspection and not issolved(self.cube):
        solve_time = f'DNS'
        tps = 'N/A'
    elif start == end:
        solve_time = '0.000'
        tps = '???'
    else:
        solve_time = end - start_time
        tps = self.movecount()['ETM'] / solve_time
        tps = f'{tps:.3f}'
        solve_time = convert_seconds(solve_time)
        if not issolved(self.cube):
            solve_time = f'DNF({solve_time})'

    stats = {
        'TIME': solve_time,
        **self.movecount(),
        'TPS': tps,
        'START TIME': time.strftime('%d %B %Y %X', time.localtime(start)),
        'END TIME': time.strftime('%d %B %Y %X', time.localtime(end))
    }

    return stats
