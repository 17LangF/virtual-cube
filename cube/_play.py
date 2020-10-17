'''
Virtual Cube Program - Made by Fred Lang.
Speedsolve method.
'''

import time

#Play
def play(self, moves, tps='AUTO'):
    size = self.size

    try:
        tps = float(tps)
    except ValueError:
        if str(tps).upper() == 'AUTO':
            if size < 4:
                tps = 3
            elif size < 8:
                tps = 10
            else:
                tps = 0
        else:
            raise TypeError

    if tps != 0:
        move_time = 1 / tps
    else:
        move_time = 0

    for move in moves:
        self.move(move)
        self.show()
        time.sleep(move_time)
