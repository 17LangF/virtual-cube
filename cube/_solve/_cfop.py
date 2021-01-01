'''
Virtual Cube Program - Made by Fred Lang.
CFOP method solver.
'''

from cube.functions import issolved, reverse

#CFOP
def cfop(self):
    solve = []
    stats = {'3x3 STAGE': 0}

    for step in cross, f2l, oll, pll:
        step_solve, step_stats = step(self)

        solve.extend(step_solve)
        stats['3x3 STAGE'] += len(step_solve)

    return solve, stats

#Cross
def cross(self):
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

#First 2 Layers
def f2l(self):
    cube = self.cube
    size = self.size
    solve = []

    corners = (
        ((0,0,0), (4,0,-1), (1,0,0)),
        ((0,0,-1), (3,0,-1), (4,0,0)),
        ((0,-1,-1), (2,0,-1), (3,0,0)),
        ((0,-1,0), (1,0,-1), (2,0,0)),
        ((5,0,0), (2,-1,0), (1,-1,-1)),
        ((5,0,-1), (3,-1,0), (2,-1,-1)),
        ((5,-1,-1), (4,-1,0), (3,-1,-1)),
        ((5,-1,0), (1,-1,0), (4,-1,-1))
    )

    edges = (
        ((0,0,1), (4,0,1)),
        ((0,1,-1), (3,0,1)),
        ((0,-1,1), (2,0,1)),
        ((0,1,0), (1,0,1)),
        ((2,1,0), (1,1,-1)),
        ((2,1,-1), (3,1,0)),
        ((4,1,0), (3,1,-1)),
        ((4,1,-1), (1,1,0))
    )

    if not hasattr(self, 'f2ls'):
        with open('docs/F2Ls.txt') as f:
            self.f2ls = [line.split(maxsplit=1) for line in f.readlines()]

    for _ in range(4):
        pairs = {pair: [] for pair in ('FR','FL','BR','BL')}
        faces = [side[1][1] for side in cube]

        #Get corner positions and orientations
        for corner in corners:
            stickers = [cube[corner[i][0]][corner[i][1]][corner[i][2]]
                        for i in range(3)]

            if 'U' not in stickers:
                continue

            pair = []
            if faces[2] in stickers:
                pair.append('F')
            else:
                pair.append('B')

            if faces[3] in stickers:
                pair.append('R')
            else:
                pair.append('L')

            pair = ''.join(pair)

            if corner[0][0] == 5:
                position = corner[2][0] + 4
            else:
                position = 5 - corner[1][0]

            orientation = stickers.index('U')

            pairs[pair].extend((position, orientation))

        #Get edge positions and orientations
        for edge in edges:
            stickers = [cube[edge[i][0]][edge[i][1]][edge[i][2]]
                        for i in range(2)]

            if 'D' in stickers:
                continue

            pair = []
            if faces[2] in stickers:
                pair.append('F')
            else:
                pair.append('B')

            if faces[3] in stickers:
                pair.append('R')
            else:
                pair.append('L')

            pair = ''.join(pair)

            if edge[0][0] != 0:
                position = 4 + edge[0][0] + edge[1][2]
            else:
                position = 5 - edge[1][0]

            orientation = int(stickers[0] in (faces[1], faces[3]))

            pairs[pair].extend((position, orientation))

        #Correct pairs
        #FL
        pairs['FL'][0] = (pairs['FL'][0] - 1 ^ 1) + 1
        pairs['FL'][1] = (3 - pairs['FL'][1]) % 3
        if pairs['FL'][2] in (2,4):
            pairs['FL'][2] = 6 - pairs['FL'][2]
        elif pairs['FL'][2] > 4:
            pairs['FL'][2] = (pairs['FL'][2] - 1 ^ 1) + 1

        #BR
        pairs['BR'][0] = (pairs['BR'][0] - 1 ^ 3) + 1
        pairs['BR'][1] = (3 - pairs['BR'][1]) % 3
        if pairs['BR'][2] in (1,3):
            pairs['BR'][2] = (pairs['BR'][2] - 1 ^ 2) + 1
        elif pairs['BR'][2] > 4:
            pairs['BR'][2] = 13 - pairs['BR'][2]

        #BL
        pairs['BL'][0] = (pairs['BL'][0] - 1 ^ 2) + 1
        pairs['BL'][2] = (pairs['BL'][2] - 1 ^ 2) + 1

        if pairs == dict.fromkeys(('FR','FL','BR','BL'), [6, 0, 6, 0]):
            break

        #Find best pair alg
        turns = []
        for turn in range(4):
            turns.append({k:v[:] for k,v in pairs.items()})
            for pair in pairs:
                for i in 0,2:
                    if pairs[pair][i] < 5:
                        pairs[pair][i] = pairs[pair][i] % 4 + 1

        def best_alg():
            for state, alg in self.f2ls:
                for turn in range(4):
                    for pair in turns[turn]:
                        if ''.join(map(str, turns[turn][pair])) == state:
                            return pair, alg, turn

        pair, alg, turns = best_alg()

        #Correct alg
        if turns:
            if turns == 1:
                setup = 'U'
            elif turns == 2:
                setup = 'U2'
            else:
                setup = "U'"
            alg = f'{setup} {alg}'

        if pair == 'FL':
            replacements = (('U',"U'"),('u',"u'"),('D',"D'"),('y',"y'"),
                            ('R','.'),('L',"R'"),('.',"L'"),('F',"F'"),
                            ("''",''),("'2", '2'))
        elif pair == 'BR':
            replacements = (('U',"U'"),('u',"u'"),('D',"D'"),('y',"y'"),
                            ('R',"R'"),('L',"L'"),('F',"B'"),
                            ("''",''),("'2", '2'))
        elif pair == 'BL':
            replacements = (('R','.'),('L','R'),('.','L'),('F','B'))
        else:
            replacements = ()

        for a,b in replacements:
            alg = alg.replace(a,b)

        if size > 3:
            alg = alg.replace('u', f'{size-1}Uw')

        #Do moves
        f2l_alg = alg.split()
        self.move(f2l_alg)
        solve.extend(f2l_alg)

    return solve, {'F2L': len(solve)}

#Orientation of the Last Layer
def oll(self):
    cube = self.cube
    size = self.size
    solve = []

    last_layer = (
        ((0,0,0), (4,0,-1), (1,0,0)),
        ((0,0,1), (4,0,1)),
        ((0,0,-1), (3,0,-1), (4,0,0)),
        ((0,1,-1), (3,0,1)),
        ((0,-1,-1), (2,0,-1), (3,0,0)),
        ((0,-1,1), (2,0,1)),
        ((0,-1,0), (1,0,-1), (2,0,0)),
        ((0,1,0), (1,0,1))
    )

    if not hasattr(self, 'olls'):
        with open('docs/OLLs.txt') as f:
            self.olls = [line.split(maxsplit=2) for line in f.readlines()]

    #OLL parity
    parity = False
    for edge in last_layer[1::2]:
        if cube[edge[0][0]][edge[0][1]][edge[0][2]] == 'D':
            parity = not parity

    if parity:
        oll_parity = "Rw' U2 Lw F2 Lw' F2 Rw2 U2 Rw U2 Rw' U2 F2 Rw2 F2"
        if size > 5:
            rw = f'{size//2}Rw'
            lw = f'{size//2}Lw'
            oll_parity = oll_parity.replace('Rw',rw).replace('Lw',lw)

        oll_parity = oll_parity.split()
        self.move(oll_parity)
        solve.extend(oll_parity)

    oll = []
    for piece in last_layer:
        for i in range(3):
            if cube[piece[i][0]][piece[i][1]][piece[i][2]] == 'D':
                oll.append(i)
                break

    oll = ''.join(map(str, oll))

    if oll != '00000000':
        for name, state, alg in self.olls:
            if state == oll:
                setup = []
            elif state == oll[-2:] + oll[:-2]:
                setup = ['U']
            elif state == oll[-4:] + oll[:-4]:
                setup = ['U2']
            elif state == oll[-6:] + oll[:-6]:
                setup = ["U'"]
            else:
                continue

            if size > 3:
                for move in 'ulfrbd':
                    alg = alg.replace(move, f'{size-1}{move.upper()}w')

                for move in 'MES':
                    alg = alg.replace(move, move.lower())

            oll_alg = setup + alg.split()
            self.move(oll_alg)
            solve.extend(oll_alg)
            break

        else:
            return False, {}

    return solve, {'OLL': len(solve)}

#Permutation of the Last Layer
def pll(self):
    cube = self.cube
    size = self.size
    solve = []

    faces = [side[1][1] for side in cube]

    if not hasattr(self, 'plls'):
        with open('docs/PLLs.txt') as f:
            self.plls = [line.split(maxsplit=2) for line in f.readlines()]

    pll = []
    for s in range(4,0,-1):
        for x in -1,1:
            pll.append((s - faces.index(cube[s][0][x])) % 4)

    counts = {turn: pll.count(turn) for turn in range(4)}

    if len(set(counts.values())) == 1:
        #G perm
        mode = max(range(4), key=pll[::2].count)
    elif len(set(counts.values())) == 2:
        #H perm / N perm
        mode = pll[0]
    else:
        #Other
        mode = max(set(pll), key=pll.count)

    pll = [(piece - mode) % 4 for piece in pll]
    pll = ''.join(map(str, pll))

    if pll != '00000000':
        #PLL Parity
        plls = [possible_pll[1] for possible_pll in self.plls]
        for shift in range(0,8,2):
            if pll[-shift:] + pll[:-shift] in plls:
                break
        else:
            pll_parity = "2R2 U2 2R2 Uw2 2R2 Uw2"
            if size > 5:
                r = f'2-{size//2}Rw2'
                uw = f'{size//2}Uw'
                pll_parity = pll_parity.replace('2R2',r).replace('Uw',uw)

            pll_parity = pll_parity.split()
            self.move(pll_parity)
            solve.extend(pll_parity)

            pll = [int(turn) for turn in pll]
            for i in 0,2,3:
                pll[i], pll[i+4] = (pll[i+4] + 2) % 4, (pll[i] + 2) % 4

            counts = {turn: pll.count(turn) for turn in range(4)}

            if len(set(counts.values())) == 1:
                #G perm
                mode = max(range(4), key=pll[::2].count)
            elif len(set(counts.values())) == 2:
                #H perm / N perm
                mode = pll[0]
            else:
                #Other
                mode = max(set(pll), key=pll.count)

            pll = [(piece - mode) % 4 for piece in pll]
            pll = ''.join(map(str, pll))

    if pll != '00000000':
        for name, state, alg in self.plls:
            if state == pll:
                setup = []
            elif state == pll[-2:] + pll[:-2]:
                setup = ['U']
            elif state == pll[-4:] + pll[:-4]:
                setup = ['U2']
            elif state == pll[-6:] + pll[:-6]:
                setup = ["U'"]
            else:
                continue

            if size > 3:
                for move in 'ulfrbd':
                    alg = alg.replace(move, f'{size-1}{move.upper()}w')

                for move in 'MES':
                    alg = alg.replace(move, move.lower())

            pll_alg = setup + alg.split()
            self.move(pll_alg)
            solve.extend(pll_alg)

            if alg[0] in 'xz':
                if not issolved(cube):
                    move = reverse(alg.split()[:1])[0]
                    self.move(move)
                    solve.append(move)
            break

        else:
            return False, {}

    #AUF
    if cube[1][0][0] != cube[1][1][1]:
        if cube[2][0][0] == cube[1][1][1]:
            move = 'U'
        elif cube[3][0][0] == cube[1][1][1]:
            move = 'U2'
        else:
            move = "U'"

        self.move(move)
        solve.append(move)

    return solve, {'PLL': len(solve)}
