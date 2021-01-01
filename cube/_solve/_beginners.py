'''
Virtual Cube Program - Made by Fred Lang.
Beginners method solver.
'''

#Beginners cross
def b_cross(self):
    cube = self.cube
    solve = []
    edges = (1,0),(-1,1),(1,-1),(0,1)

    cross = {
        'L': (4,1,-1),
        "L'": (2,1,0),
        'F': (1,1,-1),
        "F'": (3,1,0),
        'R': (2,1,-1),
        "R'": (4,1,0),
        'B': (3,1,-1),
        "B'": (1,1,0),
        'L2': (5,1,0),
        'F2': (5,0,1),
        'R2': (5,1,-1),
        'B2': (5,-1,1),
        "L U' F": (1,0,1),
        "L' U' F": (1,-1,1),
        "F U' R": (2,0,1),
        "F' U' R": (2,-1,1),
        "R' U F'": (3,0,1),
        "R U F'": (3,-1,1),
        "B' U R'": (4,0,1),
        "B U R'": (4,-1,1)
    }

    for s, side in enumerate(cube):
        if side[1][1] == 'U':
            break

    if s != 5:
        move = ('z2',"z'","x'",'z','x')[s]
        self.move(move)
        solve.append(move)

    while not(all(cube[0][y][x] == 'U' for y,x in edges) or
              all(cube[5][y][x] == 'U' for y,x in edges) and
              all(side[-1][1] == side[1][1] for side in cube[1:5])):
        for edge in cross:
            if (cube[cross[edge][0]][cross[edge][1]][cross[edge][-1]]
                == 'U'):
                break

        slot = 'LFRB'.index(edge[0])
        if cube[0][edges[slot][0]][edges[slot][1]] != 'U':
            moves = edge.split()
        elif cube[0][edges[slot-3][0]][edges[slot-3][1]] != 'U':
            moves = ['U'] + edge.split()
        elif cube[0][edges[slot-1][0]][edges[slot-1][1]] != 'U':
            moves = ["U'"] + edge.split()
        else:
            moves = ['U2'] + edge.split()

        self.move(moves)
        solve.extend(moves)

    while any(cube[5][y][x] != 'U' for y,x in edges):
        if cube[1][0][1] == cube[1][1][1] and cube[0][1][0] == 'U':
            self.move('L2')
            solve.append('L2')
        if cube[2][0][1] == cube[2][1][1] and cube[0][-1][1] == 'U':
            self.move('F2')
            solve.append('F2')
        if cube[3][0][1] == cube[3][1][1] and cube[0][1][-1] == 'U':
            self.move('R2')
            solve.append('R2')
        if cube[4][0][1] == cube[4][1][1] and cube[0][0][1] == 'U':
            self.move('B2')
            solve.append('B2')

        if any(cube[s][0][1] == cube[(s + 2) % 4 + 1][1][1] and
               cube[0][edges[s-1][0]][edges[s-1][1]] == 'U'
               for s in range(1,5)):
            self.move('U')
            solve.append('U')
        elif any(cube[s][0][1] == cube[s % 4 + 1][1][1] and
                 cube[0][edges[s-1][0]][edges[s-1][1]] == 'U'
                 for s in range(1,5)):
            self.move("U'")
            solve.append("U'")
        elif any(cube[s][0][1] == cube[(s + 1) % 4 + 1][1][1] and
                 cube[0][edges[s-1][0]][edges[s-1][1]] == 'U'
                 for s in range(1,5)):
            self.move('U2')
            solve.append('U2')

    return solve, {'CROSS': len(solve)}

#First layer
def layer1(self):
    cube = self.cube
    solve = []
    corners = (0,0),(0,-1),(-1,0),(-1,-1)

    first_layer = (
        ((0,-1,-1),(2,0,-1),(3,0,0)),
        ((0,-1,0),(1,0,-1),(2,0,0)),
        ((0,0,-1),(3,0,-1),(4,0,0)),
        ((0,0,0),(4,0,-1),(1,0,0))
    )

    while not(all(cube[5][y][x] == 'U' for y,x in corners) and
              all(len(set(side[-1])) == 1 for side in cube[1:5])):
        for corner in first_layer:
            if any(cube[x[0]][x[1]][x[2]] == 'U' for x in corner):
                break
        else:
            if cube[5][0][-1] != 'U' or cube[2][-1][-1] != cube[2][1][1]:
                pass
            elif (cube[5][0][0] != 'U' or
                  cube[1][-1][-1] != cube[1][1][1]):
                self.move("y'")
                solve.append("y'")
            elif (cube[5][-1][-1] != 'U' or
                  cube[3][-1][-1] != cube[3][1][1]):
                self.move('y')
                solve.append('y')
            else:
                self.move('y2')
                solve.append('y2')

            moves = 'R','U',"R'","U'"
            self.move(moves)
            solve.extend(moves)
            continue

        piece = []
        for x in corner:
            piece.append(cube[x[0]][x[1]][x[2]])

        slot = piece[piece.index('U')-1]
        for s, side in enumerate(cube[1:5], 1):
            if side[1][1] == slot:
                slot = s - 1
                break

        piece = corner[1][0] - 1
        turns = (piece - slot) % 4

        if turns == 1:
            self.move('U')
            solve.append('U')
        elif turns == 2:
            self.move('U2')
            solve.append('U2')
        elif turns == 3:
            self.move("U'")
            solve.append("U'")

        if slot == 0:
            self.move("y'")
            solve.append("y'")
        elif slot == 2:
            self.move('y')
            solve.append('y')
        elif slot == 3:
            self.move('y2')
            solve.append('y2')

        while cube[5][0][-1] != 'U' or cube[2][-1][-1] != cube[2][-1][1]:
            moves = 'R','U',"R'","U'"
            self.move(moves)
            solve.extend(moves)

    return solve, {'FIRST LAYER': len(solve)}

#Second layer
def layer2(self):
    cube = self.cube
    solve = []
    second_layer = (
        ((0,-1,1),(2,0,1)),
        ((0,1,-1),(3,0,1)),
        ((0,1,0),(1,0,1)),
        ((0,0,1),(4,0,1))
    )

    left_alg = "U' L' U L U F U' F'".split()
    right_alg = "U R U' R' U' F' U F".split()

    while not all(side[1][0] == side[1][1] == side[1][-1]
                  for side in cube[1:]):
        for edge in second_layer:
            if all(cube[x[0]][x[1]][x[2]] != 'D' for x in edge):
                break
        else:
            if (cube[2][1][-1] != cube[2][1][1] or
                cube[3][1][0] != cube[3][1][1]):
                moves = right_alg
            elif (cube[2][1][0] != cube[2][1][1] or
                  cube[1][1][-1] != cube[1][1][1]):
                moves = left_alg
            elif (cube[3][1][-1] != cube[3][1][1] or
                  cube[4][1][0] != cube[4][1][1]):
                self.move('y')
                solve.append('y')
                moves = right_alg
            else:
                self.move("y'")
                solve.append("y'")
                moves = left_alg

            self.move(moves)
            solve.extend(moves)
            continue

        piece = []
        for x in edge:
            piece.append(cube[x[0]][x[1]][x[2]])

        for s, side in enumerate(cube[1:5], 1):
            if side[1][1] == piece[1]:
                side = s - 1
                break

        piece = edge[1][0] - 1
        turns = (piece - side) % 4

        if turns == 1:
            self.move('U')
            solve.append('U')
        elif turns == 2:
            self.move('U2')
            solve.append('U2')
        elif turns == 3:
            self.move("U'")
            solve.append("U'")

        if side == 0:
            self.move("y'")
            solve.append("y'")
        elif side == 2:
            self.move('y')
            solve.append('y')
        elif side == 3:
            self.move('y2')
            solve.append('y2')

        if cube[0][-1][1] == cube[1][1][1]:
            moves = left_alg
        else:
            moves = right_alg

        self.move(moves)
        solve.extend(moves)

    return solve, {'SECOND LAYER': len(solve)}

#Last layer cross
def eo(self):
    cube = self.cube
    size = self.size
    solve = []
    edges = (1,0),(-1,1),(1,-1),(0,1)
    eo_alg = "F R U R' U' F'".split()

    while any(cube[0][y][x] != 'D' for y,x in edges):
        pieces = tuple(i for i in range(4)
                       if cube[0][edges[i][0]][edges[i][1]] == 'D')
        setups = {
            (0,1,2): 'U2',
            (0,1,3): 'U',
            (1,2,3): "U'",
            (0,1): "U'",
            (0,3): 'U2',
            (1,3): 'U',
            (2,3): 'U',
            (1,): 'U'
        }

        if pieces in setups:
            self.move(setups[pieces])
            solve.append(setups[pieces])

        #OLL parity
        if len(pieces) % 2:
            oll_parity = "Rw' U2 Lw F2 Lw' F2 Rw2 U2 Rw U2 Rw' U2 F2 Rw2 F2"
            if size > 5:
                rw = f'{size//2}Rw'
                lw = f'{size//2}Lw'
                oll_parity = oll_parity.replace('Rw',rw).replace('Lw',lw)

            oll_parity = oll_parity.split()
            self.move(oll_parity)
            solve.extend(oll_parity)
        else:
            self.move(eo_alg)
            solve.extend(eo_alg)

    return solve, {'LAST LAYER CROSS': len(solve)}

#Last layer face
def co(self):
    cube = self.cube
    solve = []
    corners = (0,0),(0,-1),(-1,0),(-1,-1)

    if any(cube[0][y][x] != 'D' for y,x in corners):
        self.move('z2')
        solve.append('z2')

    while any(cube[5][y][x] != cube[5][1][1] for y,x in corners):
        if cube[5][0][-1] != 'D':
            pass
        elif cube[5][0][0] != 'D':
            self.move('D')
            solve.append('D')
        elif cube[5][-1][-1] != 'D':
            self.move("D'")
            solve.append("D'")
        else:
            self.move('D2')
            solve.append('D2')

        while cube[5][0][-1] != 'D':
            moves = 'R','U',"R'","U'"
            self.move(moves)
            solve.extend(moves)

    if cube[0][1][1] == 'U':
        self.move('z2')
        solve.append('z2')

    return solve, {'LAST LAYER FACE': len(solve)}

#Last layer corners
def cp(self):
    cube = self.cube
    solve = []
    cp_alg = "R U R' U' R' F R2 U' R' U' R U R' F'".split()

    for s, side in enumerate(cube[1:5], 1):
        if side[0][0] == side[0][-1]:
            break
    else:
        self.move(cp_alg)
        solve.extend(cp_alg)
        s = 3

    piece = s - 1
    for s, side in enumerate(cube[1:5], 1):
        if side[1][1] == cube[piece + 1][0][0]:
            side = s - 1
            break

    turns = (piece - side) % 4

    if turns == 1:
        self.move('U')
        solve.append('U')
    elif turns == 2:
        self.move('U2')
        solve.append('U2')
    elif turns == 3:
        self.move("U'")
        solve.append("U'")

    if any(cube[s][0][0] != cube[s][0][-1] for s in (1,2)):
        if side == 1:
            self.move('y')
            solve.append('y')
        elif side == 2:
            self.move('y2')
            solve.append('y2')
        elif side == 3:
            self.move("y'")
            solve.append("y'")

        self.move(cp_alg)
        solve.extend(cp_alg)

    return solve, {'LAST LAYER CORNERS': len(solve)}

#Last layer edges
def ep(self):
    cube = self.cube
    size = self.size
    solve = []
    ep_alg = "F2 U M' U2 M U F2"

    if size > 3:
        ep_alg = ep_alg.replace('M','m')
    ep_alg = ep_alg.split()

    while any(side[0][0] != side[0][1] for side in cube[1:5]):
        pieces = tuple(s for s, side in enumerate(cube[1:5], 1)
                       if side[0][0] == side[0][1])
        setups = {
            (2,4): 'y',
            (1,): 'y',
            (2,): 'y2',
            (3,): "y'"
        }

        if pieces in setups:
            self.move(setups[pieces])
            solve.append(setups[pieces])

        #PLL parity
        if len(pieces) == 2:
            pll_parity = "2R2 U2 2R2 Uw2 2R2 Uw2 U2"
            if size > 5:
                r = f'2-{size//2}Rw2'
                uw = f'{size//2}Uw'
                pll_parity = pll_parity.replace('2R2',r).replace('Uw',uw)

            pll_parity = pll_parity.split()
            self.move(pll_parity)
            solve.extend(pll_parity)
        else:
            self.move(ep_alg)
            solve.extend(ep_alg)

    return solve, {'LAST LAYER EDGES': len(solve)}
