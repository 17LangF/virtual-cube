'''
Virtual Cube Program - Made by Fred Lang.
Cage method solver.
'''

from cube.functions import orient

#4x4+ edges
def edges(self):
    cube = self.cube
    size = self.size
    solve = []
    mid = size // 2

    edges = {
        'FL': ((2,'+',0), (1,'+',-1), 'FL'),
        'BL': ((4,'+',-1), (1,'+',0), 'BL'),
        'BR': ((4,'+',0), (3,'+',-1), 'BR'),
        'UF': ((0,-1,'+'), (2,0,'+'), "L' U L"),
        'UR': ((0,'+',-1), (3,0,'-'), "F U F'"),
        'UL': ((0,'+',0), (1,0,'+'), "F U' F'"),
        'UB': ((0,0,'+'), (4,0,'-'), "L' U' L"),
        'DF': ((5,0,'+'), (2,-1,'+'), "L D' L'"),
        'DR': ((5,'+',-1), (3,-1,'+'), "F' D' F"),
        'DL': ((5,'+',0), (1,-1,'-'), "F' D F"),
        'DB': ((5,-1,'+'), (4,-1,'-'), "L D L'"),
        'FR': ((2,'+',-1), (3,'+',0), 'FR')
    }

    flip = "R U R' F R' F' R".split()

    #First 9 edges
    while True:
        f,r = cube[2][mid][-1], cube[3][mid][0]
        fr = tuple(cube[2][y][-1] for y in range(1,size-1))
        rf = tuple(cube[3][y][0] for y in range(1,size-1))

        #If FR edge is solved
        if fr.count(f) == rf.count(r) == size - 2:
            for edge in edges.values():
                if 0 < edge[0][0] < 5:
                    continue

                a, b = edge[:2]
                if isinstance(a[1], int):
                    a = tuple(cube[a[0]][a[1]][y] for y in range(1,size-1))
                else:
                    a = tuple(cube[a[0]][y][a[2]] for y in range(1,size-1))

                if isinstance(b[1], int):
                    b = tuple(cube[b[0]][b[1]][y] for y in range(1,size-1))
                else:
                    b = tuple(cube[b[0]][y][b[2]] for y in range(1,size-1))

                if a.count(a[0]) == b.count(b[0]) == size - 2:
                    continue

                moves = edge[2]

                if 'F' in moves:
                    moves = moves.replace('F', "F'").replace("''", '')
                else:
                    moves = moves.replace('L', "R'").replace('U', "U'")
                    moves = moves.replace('D', "D'").replace("''", '')

                moves = moves.split()
                self.move(moves)
                solve.extend(moves)
                break

            else:
                #No empty slots on U or D layer
                break

            continue

        #Find unsolved edge
        for edge in edges.values():
            for i in range(1,size-1):
                sticker1 = list(edge[0])
                if '+' in sticker1:
                    sticker1[sticker1.index('+')] = i
                else:
                    sticker1[sticker1.index('-')] = size - i - 1
                sticker1 = cube[sticker1[0]][sticker1[1]][sticker1[2]]

                sticker2 = list(edge[1])
                if '+' in sticker2:
                    sticker2[sticker2.index('+')] = i
                else:
                    sticker2[sticker2.index('-')] = size - i - 1
                sticker2 = cube[sticker2[0]][sticker2[1]][sticker2[2]]

                if {sticker1, sticker2} == {f,r}:
                    break
            else:
                continue
            break

        #Do moves
        if len(edge[2]) != 2:
            moves = edge[2].split()
            self.move(moves)
            solve.extend(moves)
            edge = 'FL'
        else:
            edge = edge[2]

        if edge == 'BR':
            for y in range(1,size-1):
                if cube[3][y][-1] == f and cube[4][y][0] == r:
                    move = f'{y+1}U'
                    self.move(move)
                    solve.append(move)

            for y in range(1,size-1):
                if cube[3][y][-1] == r and cube[4][y][0] == f:
                    self.move('B2')
                    solve.append('B2')
                edge = 'BL'

        if edge == 'BL':
            for y in range(1,size-1):
                if cube[4][y][-1] == f and cube[1][y][0] == r:
                    move = f'{y+1}U2'
                    self.move(move)
                    solve.append(move)

            for y in range(1,size-1):
                if cube[4][y][-1] == r and cube[1][y][0] == f:
                    self.move('L2')
                    solve.append('L2')
                edge = 'FL'

        if edge == 'FL':
            for y in range(1,size-1):
                if cube[1][y][-1] == f and cube[2][y][0] == r:
                    move = f"{y+1}U'"
                    self.move(move)
                    solve.append(move)

            for y in range(1,size-1):
                if cube[1][y][-1] == r and cube[2][y][0] == f:
                    self.move('L2')
                    solve.append('L2')

                for y in range(1,size-1):
                    if cube[4][y][-1] == f and cube[1][y][0] == r:
                        move = f'{y+1}U2'
                        self.move(move)
                        solve.append(move)

        #Flipped edge
        if edge == 'FR':
            depths = []
            for y in range(1,size-1):
                if cube[2][y][-1] != f:
                    depths.append(y)

            for y in depths:
                move = f'{y+1}U'
                self.move(move)
                solve.append(move)

            self.move(flip)
            solve.extend(flip)

            for y in depths:
                move = f"{y+1}U'"
                self.move(move)
                solve.append(move)

    #Last 3 edges
    self.move('y')
    solve.append('y')

    edges = ((3,'+',-1), (4,'+',0), 1), ((4,'+',-1), (1,'+',0), 2)

    for solving_edge in range(2):
        if solving_edge == 1:
            edges = edges[:1]
        f,r = cube[2][mid][-1], cube[3][mid][0]

        for edge in edges:
            #Do moves
            depths = [[],[]]
            for y in range(1,size-1):
                sticker1 = cube[edge[0][0]][y][edge[0][2]]
                sticker2 = cube[edge[1][0]][y][edge[1][2]]

                if {sticker1, sticker2} == {f,r}:
                    if {cube[2][-y-1][-1], cube[3][-y-1][0]} == {f,r}:
                        depths[1].append(y)
                    elif size-y-1 in depths[0]:
                        depths[1].append(y)
                    else:
                        depths[0].append(y)

            for i in range(2):
                if depths[i]:
                    for y in depths[i]:
                        if edge[2] == 1:
                            move = f'{y+1}U'
                        else:
                            move = f'{y+1}U2'
                        self.move(move)
                        solve.append(move)

                    self.move(flip)
                    solve.extend(flip)

                    for y in depths[i]:
                        if edge[2] == 1:
                            move = f"{y+1}U'"
                        else:
                            move = f'{y+1}U2'
                        self.move(move)
                        solve.append(move)

                elif depths[1]:
                    self.move(flip)
                    solve.extend(flip)

        #Flipped edge
        depths = [y for y in range(1,size-1) if cube[2][y][-1] == f]

        if len(depths) > size / 2 - 1:
            depths = set(range(1,size-1)) - set(depths)

        if depths:
            for y in depths:
                move = f'{y+1}U'
                self.move(move)
                solve.append(move)

            self.move(flip)
            solve.extend(flip)

            for y in depths:
                move = f"{y+1}U'"
                self.move(move)
                solve.append(move)

        self.move('y')
        solve.append('y')

    #Parity
    parity = "R' U2 L F2 L' F2 R2 U2 R U2 R' U2 F2 R2 F2"

    f = cube[2][mid][-1]
    depths = [y for y in range(1,size//2) if cube[2][y][-1] != f]

    if len(depths) > size / 2 - 1 and not size % 2:
        depths = set(range(1,size-1)) - set(depths)

    if depths:
        self.move("z'")
        solve.append("z'")
        ri = ''.join(f"{depth+1}R' " for depth in depths)
        li = ''.join(f"{depth+1}L' " for depth in depths)
        r2 = ''.join(f'{depth+1}R2 ' for depth in depths)
        r = ''.join(f'{depth+1}R ' for depth in depths)
        l = ''.join(f'{depth+1}L ' for depth in depths)

        parity = parity.replace("R' ",ri).replace("L' ",li).replace('R2 ',r2)
        parity = parity.replace('R ',r).replace('L ',l)

        parity = parity.split()
        self.move(parity)
        solve.extend(parity)

    return solve, {'EDGES': len(solve)}

#4x4+ centres
def centres(self):
    cube = self.cube
    size = self.size
    stats = {}
    total_centres = (size - 2) ** 2
    mid = size // 2

    if size % 2:
        solve = orient(cube)
        self.move(solve)
    else:
        solve = []

    for side in 'UDLFR':
        count = sum(cube[0][y][1:-1].count(side) for y in range(1,size-1))

        while count < total_centres:
            for s in 2,1,3,4,5:
                if sum(cube[s][y][1:-1].count(side) for y in range(1,size-1)):
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

                        self.move(moves)
                        solve.extend(moves)

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
