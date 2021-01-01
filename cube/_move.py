'''
Virtual Cube Program - Made by Fred Lang.
Move method.
'''

from cube.functions import reverse, parse_moves, split_move

#Move
def move(self, moves):
    size = self.size

    if isinstance(moves, str):
        moves = [moves]

    split_moves = [split_move(move, size) for move in moves]
    self.moves.extend(moves)

    for depth, face, turns in split_moves:
        turns %= 4

        if not turns:
            continue

        if face in 'RBD':
            if face == 'R':
                face = 'L'
            elif face == 'B':
                face = 'F'
            else:
                face = 'U'

            depth = [size - depth[1], size - depth[0]]
            turns = 4 - turns

        def rotate(square, turns):
            if turns == 1:
                return [list(i) for i in zip(*square[::-1])]
            elif turns == 2:
                return [i[::-1] for i in square[::-1]]
            else:
                return [list(i) for i in list(zip(*square))[::-1]]

        #Turns cube
        cube = self.cube

        if face == 'U':
            if depth[0] == 0:
                cube[0] = rotate(cube[0], turns)

            for y in range(*depth):
                if turns == 1:
                    cube[1][y], cube[2][y], cube[3][y], cube[4][y] = \
                    cube[2][y], cube[3][y], cube[4][y], cube[1][y]
                elif turns == 2:
                    cube[1][y], cube[2][y], cube[3][y], cube[4][y] = \
                    cube[3][y], cube[4][y], cube[1][y], cube[2][y]
                else:
                    cube[1][y], cube[2][y], cube[3][y], cube[4][y] = \
                    cube[4][y], cube[1][y], cube[2][y], cube[3][y]

            if depth[1] == size:
                cube[5] = rotate(cube[5], 4 - turns)

        elif face == 'L':
            if depth[0] == 0:
                cube[1] = rotate(cube[1], turns)

            columns = {s: list(zip(*cube[s])) for s in [0,2,5,4]}

            for x in range(*depth):
                for y in range(size):
                    if turns == 1:
                        cube[0][y][x] = columns[4][-x-1][-y-1]
                        cube[2][y][x] = columns[0][x][y]
                        cube[5][y][x] = columns[2][x][y]
                        cube[4][y][-x-1] = columns[5][x][-y-1]
                    elif turns == 2:
                        cube[0][y][x] = columns[5][x][y]
                        cube[2][y][x] = columns[4][-x-1][-y-1]
                        cube[5][y][x] = columns[0][x][y]
                        cube[4][y][-x-1] = columns[2][x][-y-1]
                    else:
                        cube[0][y][x] = columns[2][x][y]
                        cube[2][y][x] = columns[5][x][y]
                        cube[5][y][x] = columns[4][-x-1][-y-1]
                        cube[4][y][-x-1] = columns[0][x][-y-1]

            if depth[1] == size:
                cube[3] = rotate(cube[3], 4 - turns)

        else:
            if depth[0] == 0:
                cube[2] = rotate(cube[2], turns)

            columns = {s: list(zip(*cube[s])) for s in [1,3]}

            for x in range(*depth):
                for y in range(size):
                    if turns == 1:
                        cube[1][y][-x-1] = cube[5][x][y]
                        cube[3][y][x] = cube[0][-x-1][y]
                    elif turns == 2:
                        cube[1][y][-x-1] = list(columns[3][x])[-y-1]
                        cube[3][y][x] = list(columns[1][-x-1])[-y-1]
                    else:
                        cube[1][y][-x-1] = cube[0][-x-1][-y-1]
                        cube[3][y][x] = cube[5][x][-y-1]

                if turns == 1:
                    cube[0][-x-1] = list(columns[1][-x-1])[::-1]
                    cube[5][x] = list(columns[3][x])[::-1]
                elif turns == 2:
                    cube[0][-x-1], cube[5][x] = \
                    cube[5][x][::-1], cube[0][-x-1][::-1]
                else:
                    cube[0][-x-1] = list(columns[3][x])
                    cube[5][x] = list(columns[1][-x-1])

            if depth[1] == size:
                cube[4] = rotate(cube[4], 4 - turns)

    return moves
