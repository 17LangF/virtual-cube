'''
Virtual Cube Program - Made by Fred Lang.
Move method.
'''

from cube.functions import split_move

#Move
def move(self, move):
    size = self.size

    if not split_move(move, size):
        return False

    self.moves.append(move)

    depth, face, turns = split_move(move, size)

    #Turns cube
    for turn in range(turns % 4):
        cube = [[y[:] for y in s] for s in self.cube]

        if face == 'U':
            if depth[0] == 0:
                self.cube[0] = [list(i) for i in zip(*cube[0][::-1])]
            for y in range(*depth):
                self.cube[1][y] = cube[2][y]
                self.cube[2][y] = cube[3][y]
                self.cube[3][y] = cube[4][y]
                self.cube[4][y] = cube[1][y]
            if depth[1] == size:
                self.cube[5] = [list(i) for i in list(zip(*cube[5]))[::-1]]

        elif face == 'L':
            if depth[0] == 0:
                self.cube[1] = [list(i) for i in zip(*cube[1][::-1])]
            for x in range(*depth):
                for y in range(size):
                    self.cube[0][y][x] = list(zip(*cube[4]))[-x-1][-y-1]
                    self.cube[2][y][x] = list(zip(*cube[0]))[x][y]
                    self.cube[4][y][-x-1] = list(zip(*cube[5]))[x][-y-1]
                    self.cube[5][y][x] = list(zip(*cube[2]))[x][y]
            if depth[1] == size:
                self.cube[3] = [list(i) for i in list(zip(*cube[3]))[::-1]]

        elif face == 'F':
            if depth[0] == 0:
                self.cube[2] = [list(i) for i in zip(*cube[2][::-1])]
            for x in range(*depth):
                self.cube[0][-x-1] = list(list(zip(*cube[1]))[-x-1])[::-1]
                self.cube[5][x] = list(list(zip(*cube[3]))[x])[::-1]
                for y in range(size):
                    self.cube[1][y][-x-1] = cube[5][x][y]
                    self.cube[3][y][x] = cube[0][-x-1][y]
            if depth[1] == size:
                self.cube[4] = [list(i) for i in list(zip(*cube[4]))[::-1]]

        elif face == 'R':
            if depth[0] == 0:
                self.cube[3] = [list(i) for i in zip(*cube[3][::-1])]
            for x in range(*depth):
                for y in range(size):
                    self.cube[0][y][-x-1] = list(zip(*cube[2]))[-x-1][y]
                    self.cube[2][y][-x-1] = list(zip(*cube[5]))[-x-1][y]
                    self.cube[4][y][x] = list(zip(*cube[0]))[-x-1][-y-1]
                    self.cube[5][y][-x-1] = list(zip(*cube[4]))[x][-y-1]
            if depth[1] == size:
                self.cube[1] = [list(i) for i in list(zip(*cube[1]))[::-1]]

        elif face == 'B':
            if depth[0] == 0:
                self.cube[4] = [list(i) for i in zip(*cube[4][::-1])]
            for x in range(*depth):
                self.cube[0][x] = list(list(zip(*cube[3]))[-x-1])
                self.cube[5][-x-1] = list(list(zip(*cube[1]))[x])
                for y in range(size):
                    self.cube[1][y][x] = cube[0][x][-y-1]
                    self.cube[3][y][-x-1] = cube[5][-x-1][-y-1]
            if depth[1] == size:
                self.cube[2] = [list(i) for i in list(zip(*cube[2]))[::-1]]

        elif face == 'D':
            if depth[0] == 0:
                self.cube[5] = [list(i) for i in zip(*cube[5][::-1])]
            for y in range(*depth):
                self.cube[1][-y-1] = cube[4][-y-1]
                self.cube[2][-y-1] = cube[1][-y-1]
                self.cube[3][-y-1] = cube[2][-y-1]
                self.cube[4][-y-1] = cube[3][-y-1]
            if depth[1] == size:
                self.cube[0] = [list(i) for i in list(zip(*cube[0]))[::-1]]

        else:
            self.moves.pop()
            return False

    return True
