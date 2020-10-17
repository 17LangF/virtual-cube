'''
Virtual Cube Program - Made by Fred Lang.
Cage method solver.
'''

#4x4+ centres
def centres(self):
    cube = self.cube
    size = self.size
    stats = {}
    total_centres = (size - 2) ** 2
    mid = size // 2

    if size % 2:
        solve = self.orient()
        for move in solve:
            self.move(move)
    else:
        solve = []

    for side in 'UDLFR':
        count = sum(cube[0][y][1:-1].count(side) for y in range(1,size-1))

        while count < total_centres:
            for s in 2,1,3,4,5:
                if sum(cube[s][y][1:-1].count(side)
                       for y in range(1,size-1)):
                    break

            if s == 1:
                self.move("y'")
                solve.append("y'")
                s = 2
            elif s == 3:
                self.move('y')
                solve.append('y')
                s = 2
            elif s == 4:
                self.move('y2')
                solve.append('y2')
                s = 2

            for y in range(1,size-1):
                for x in range(1,size-1):
                    if cube[s][y][x] == side:

                        if cube[0][y][x] != side:
                            setup = ''
                        elif cube[0][size - x - 1][y] != side:
                            setup = 'U'
                        elif cube[0][x][size - y - 1] != side:
                            setup = "U'"
                        else:
                            setup = 'U2'

                        if setup:
                            self.move(setup)
                            solve.append(setup)

                        if y < mid:
                            y = str(y + 1)
                            if x < mid:
                                x = str(x + 1)
                                moves = (x + "L'", 'U', y + 'R', "U'",
                                         x + 'L', 'U', y + "R'", "U'")
                            else:
                                x = str(size - x)
                                moves = (x + 'R', "U'", y + "L'", 'U',
                                         x + "R'", "U'", y + 'L', 'U')
                        else:
                            y = str(size - y)
                            if x < mid:
                                x = str(x + 1)
                                moves = (x + "L'", "U'", y + 'R', 'U',
                                         x + 'L', "U'", y + "R'", 'U')
                            else:
                                x = str(size - x)
                                moves = (x + 'R', 'U', y + "L'", "U'",
                                         x + "R'", 'U', y + 'L', "U'")

                        if s == 5:
                            moves = ' '.join(moves)
                            moves = moves.replace('L', 'L2')
                            moves = moves.replace('R', 'R2')
                            moves = moves.replace("2'", '2')
                            moves = moves.split()

                        for move in moves:
                            self.move(move)
                            solve.append(move)

                        if setup == 'U':
                            setup = "U'"
                        elif setup == "U'":
                            setup = 'U'

                        if setup:
                            self.move(setup)
                            solve.append(setup)

                        break
                else:
                    continue
                break

            count += 1

        stats[side+' CENTRE'] = len(solve) - sum(stats.values())

        if side == 'U':
            self.move('z2')
            solve.append('z2')

        elif side == 'D':
            self.move("z'")
            solve.append("z'")

            if size % 2:
                if cube[0][mid][mid] == 'B':
                    self.move('x')
                    solve.append('x')
                elif cube[0][mid][mid] == 'F':
                    self.move("x'")
                    solve.append("x'")
                elif cube[0][mid][mid] == 'R':
                    self.move('x2')
                    solve.append('x2')

        elif side in 'LF':
            if cube[1][1][1] == 'U':
                self.move('y2')
                solve.append('y2')
            self.move('x')
            solve.append('x')

    return solve, stats
