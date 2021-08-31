"""Solve the cube as fast as you can and give statistics on solve."""

import os
import time

from cube.functions import convert_seconds, issolved, parse_moves


def speedsolve(self) -> dict:
    """
    Solve the cube as fast as you can and give statistics on solve.

    The cube is scrambled with the default method, and will start timing
    once the first turn is made, or once 15 seconds (inspection) is
    reached.

    Enter moves to solve the cube. Other functions include:
        EXIT: end solve.
        TIME: return current solving time.

    Solve times are shown in the format
    days:hours:minutes:seconds.milliseconds with leading 0s removed.

    Returns
    -------
    dict of {str: str}
        Statistics on the solve, including:
            'TIME': result of the solve, either time, DNF(time) or DNS.
            'MOVECOUNT': move count of solve in HTM, QTM, STM, and ETM.
            'TPS': average turns per second, calculated using ETM. If
            the result was DNS, TPS = 'N/A', if no time was used, TPS =
            '???'
            'START TIME': time the cube is first seen.
            'END TIME': time solve is ended.
    """

    from cube import MoveError

    self.scramble()
    os.system('cls')
    print()
    self.show()
    start = time.time()
    start_time = start
    inspection = True

    while not issolved(self.cube):
        moves = input('\nEnter move(s): ').strip()
        os.system('cls')

        if inspection:
            if time.time() > start + 15:
                start_time += 15
                inspection = False

        if moves.upper() == 'EXIT':
            break

        elif moves.upper() == 'TIME':
            if inspection:
                solve_time = convert_seconds(time.time() - start)
                print(f"INSPECTION: {solve_time}")
            else:
                solve_time = convert_seconds(time.time() - start_time)
                print(f"TIME: {solve_time}")

            print()
            self.show()
            continue

        if inspection:
            start_time = time.time()
            inspection = False

        try:
            moves = parse_moves(moves)
            self.move(moves)
        except MoveError as e:
            print(e)

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
