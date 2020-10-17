'''
Virtual Cube Program - Made by Fred Lang.
Speedsolve method.
'''

import os
import time

from cube.functions import convert_seconds, issolved

#Speedsolve
def speedsolve(self):
    print()
    self.scramble()
    self.show()

    start = time.time()
    inspection = True

    while not issolved(self.cube):
        move = input('\nEnter move(s): ').strip()
        os.system('cls')

        if inspection:
            if time.time() > start + 15:
                start_time = start + 15
                inspection = False

        if move.upper() == 'EXIT':
            break

        elif move.upper() == 'TIME':
            if inspection:
                solve_time = convert_seconds(time.time() - start)
                print(f'INSPECTION: {solve_time}')
            else:
                solve_time = convert_seconds(time.time() - start_time)
                print(f'TIME: {solve_time}')

            print()
            self.show()
            continue

        for move in move.split():
            if not self.move(move):
                print(f'{move} is invalid.')

        if inspection:
            start_time = time.time()
            inspection = False

        print()
        self.show()

    end = time.time()

    if inspection and not issolved(self.cube):
        solve_time = f'DNS'
        tps = 'N/A'
    elif start == end:
        solve_time = '0.000'
        tps = '???'
    else:
        solve_time = end - start_time
        tps = round(self.movecount()['ETM'] / solve_time, 3)
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
